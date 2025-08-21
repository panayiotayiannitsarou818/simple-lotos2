import pandas as pd
from typing import Tuple, List


def validate_excel_structure(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Ελέγχει την δομή του Excel αρχείου.
    
    Args:
        df: DataFrame προς έλεγχο
        
    Returns:
        Tuple με (is_valid, error_list)
    """
    required_columns = [
        "ΟΝΟΜΑ", "ΦΥΛΟ", "ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ", "ΖΩΗΡΟΣ", 
        "ΙΔΙΑΙΤΕΡΟΤΗΤΑ", "ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ", "ΦΙΛΟΙ", 
        "ΣΥΓΚΡΟΥΣΗ", "ΤΜΗΜΑ"
    ]
    
    errors = []
    
    # Check for required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        errors.append(f"Λείπουν στήλες: {', '.join(missing_cols)}")
    
    # Check if DataFrame is empty
    if df.empty:
        errors.append("Το αρχείο είναι κενό")
        return False, errors
    
    # Check data types and values
    if "ΦΥΛΟ" in df.columns:
        invalid_genders = df[~df["ΦΥΛΟ"].str.upper().isin(["Α", "Κ", "A", "K"])]["ΦΥΛΟ"].dropna()
        if not invalid_genders.empty:
            errors.append(f"Μη έγκυρες τιμές στο ΦΥΛΟ: {list(invalid_genders.unique())}")
    
    # Check for essential binary fields
    binary_fields = ["ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ", "ΖΩΗΡΟΣ", "ΙΔΙΑΙΤΕΡΟΤΗΤΑ", "ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ"]
    for field in binary_fields:
        if field in df.columns:
            invalid_values = df[~df[field].str.upper().isin(["Ν", "Ο", "N", "O"])][field].dropna()
            if not invalid_values.empty:
                errors.append(f"Μη έγκυρες τιμές στο {field}: {list(invalid_values.unique())}")
    
    # Check for empty ΤΜΗΜΑ
    if "ΤΜΗΜΑ" in df.columns:
        empty_tmima = df["ΤΜΗΜΑ"].isna().sum()
        if empty_tmima > 0:
            errors.append(f"Βρέθηκαν {empty_tmima} μαθητές χωρίς ΤΜΗΜΑ")
    
    return len(errors) == 0, errors


def get_validation_errors(df: pd.DataFrame) -> List[str]:
    """
    Επιστρέφει λίστα με σφάλματα validation.
    
    Args:
        df: DataFrame προς έλεγχο
        
    Returns:
        List με error messages
    """
    _, errors = validate_excel_structure(df)
    return errors
