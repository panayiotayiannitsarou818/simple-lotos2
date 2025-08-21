import pandas as pd
from io import BytesIO
from typing import Tuple


def generate_statistics_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Δημιουργεί ενιαίο πίνακα στατιστικών ανά τμήμα.
    Περιλαμβάνει μόνο όσους έχουν Ν ή Α/Κ στα αντίστοιχα πεδία.
    
    Args:
        df: DataFrame με δεδομένα μαθητών
        
    Returns:
        DataFrame με στατιστικά ανά τμήμα
    """
    df = df.copy()
    
    # Καθαρισμός δεδομένων - uppercase για συνέπεια
    df['ΦΥΛΟ'] = df['ΦΥΛΟ'].str.upper().str.strip()
    df['ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ'] = df['ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ'].str.upper().str.strip()
    df['ΖΩΗΡΟΣ'] = df['ΖΩΗΡΟΣ'].str.upper().str.strip()
    df['ΙΔΙΑΙΤΕΡΟΤΗΤΑ'] = df['ΙΔΙΑΙΤΕΡΟΤΗΤΑ'].str.upper().str.strip()
    df['ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ'] = df['ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ'].str.upper().str.strip()

    # Κανονικοποίηση φύλου: Α / Κ
    boys = df[df["ΦΥΛΟ"] == "Α"].groupby("ΤΜΗΜΑ").size()
    girls = df[df["ΦΥΛΟ"] == "Κ"].groupby("ΤΜΗΜΑ").size()

    # Ναι = Ν για τα υπόλοιπα χαρακτηριστικά
    educators = df[df["ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ"] == "Ν"].groupby("ΤΜΗΜΑ").size()
    energetic = df[df["ΖΩΗΡΟΣ"] == "Ν"].groupby("ΤΜΗΜΑ").size()
    special = df[df["ΙΔΙΑΙΤΕΡΟΤΗΤΑ"] == "Ν"].groupby("ΤΜΗΜΑ").size()
    greek = df[df["ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ"] == "Ν"].groupby("ΤΜΗΜΑ").size()
    total = df.groupby("ΤΜΗΜΑ").size()

    # Ενοποίηση
    stats = pd.DataFrame({
        "ΑΓΟΡΙΑ": boys,
        "ΚΟΡΙΤΣΙΑ": girls,
        "ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ": educators,
        "ΖΩΗΡΟΙ": energetic,
        "ΙΔΙΑΙΤΕΡΟΤΗΤΑ": special,
        "ΓΝΩΣΗ ΕΛΛ.": greek,
        "ΣΥΝΟΛΟ": total
    }).fillna(0).astype(int)

    # Ταξινόμηση ΤΜΗΜΑτων
    try:
        stats = stats.sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(float))
    except:
        stats = stats.sort_index()

    return stats


def export_statistics_to_excel(stats_df: pd.DataFrame) -> BytesIO:
    """
    Επιστρέφει BytesIO αντικείμενο με τα στατιστικά σε μορφή Excel.
    
    Args:
        stats_df: DataFrame με στατιστικά
        
    Returns:
        BytesIO object με Excel file
    """
    output = BytesIO()
    
    try:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            stats_df.to_excel(writer, index=True, sheet_name='Στατιστικά', index_label='ΤΜΗΜΑ')
            
            # Format the worksheet
            workbook = writer.book
            worksheet = writer.sheets['Στατιστικά']
            
            # Add header format
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Apply formatting to headers
            for col_num, value in enumerate(['ΤΜΗΜΑ'] + list(stats_df.columns)):
                worksheet.write(0, col_num, value, header_format)
            
            # Auto-adjust column widths
            worksheet.set_column(0, len(stats_df.columns), 15)
            
    except Exception as e:
        # Fallback to basic export
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            stats_df.to_excel(writer, index=True, sheet_name='Στατιστικά')
    
    output.seek(0)
    return output
