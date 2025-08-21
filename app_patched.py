#!/usr/bin/env python3
"""
Streamlit εφαρμογή για στατιστικά μαθητών Α' Δημοτικού.
"""

import streamlit as st
import pandas as pd
from utils.statistics_generator import generate_statistics_table, export_statistics_to_excel
from utils.data_validator import validate_excel_structure


def main():
    """Κύρια function της εφαρμογής."""
    st.set_page_config(
        page_title="Στατιστικά Μαθητών Α' Δημοτικού", 
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Στατιστικά Μαθητών Α' Δημοτικού")
    
    # Copyright notice
    st.sidebar.markdown("""
    **© 2024 - Στατιστικά Μαθητών**  
    Πνευματικά δικαιώματα διατηρούνται.
    """)
    
    # Terms acceptance check
    if "terms_accepted" not in st.session_state:
        st.session_state.terms_accepted = False
    
    if not st.session_state.terms_accepted:
        show_terms_page()
        return
    
    # Application control
    if st.sidebar.button("🔄 Επανεκκίνηση", type="secondary"):
        reset_application()
        st.rerun()
    
    # Main application flow
    st.markdown("---")
    
    # Step 1: File Upload
    st.header("📁 Βήμα 1: Εισαγωγή Excel")
    uploaded_file = st.file_uploader(
        "Επιλέξτε το αρχείο Excel με τα δεδομένα μαθητών:",
        type=["xlsx", "xls"],
        help="Το αρχείο πρέπει να περιέχει τις απαιτούμενες στήλες"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Validate structure
            is_valid, errors = validate_excel_structure(df)
            
            if not is_valid:
                st.error("❌ Σφάλμα στη δομή του αρχείου:")
                for error in errors:
                    st.error(f"• {error}")
                return
            
            st.success("✅ Το αρχείο φορτώθηκε επιτυχώς!")
            
            # Show data preview
            with st.expander("👀 Προεπισκόπηση Δεδομένων"):
                st.dataframe(df.head(10))
                st.info(f"Συνολικά μαθητές: {len(df)} | Τμήματα: {df['ΤΜΗΜΑ'].nunique()}")
            
            # Step 2: Generate Statistics
            st.header("📊 Βήμα 2: Δημιουργία Στατιστικών")
            
            if st.button("📈 Δημιουργία Πίνακα Στατιστικών", type="primary"):
                with st.spinner("Δημιουργία στατιστικών..."):
                    stats_df = generate_statistics_table(df)
                
                st.success("✅ Ο πίνακας στατιστικών δημιουργήθηκε!")
                
                # Display statistics
                st.subheader("📋 Πίνακας Στατιστικών")
                st.dataframe(stats_df, use_container_width=True)
                
                # Step 3: Export
                st.header("💾 Βήμα 3: Εξαγωγή Πίνακα")
                
                excel_buffer = export_statistics_to_excel(stats_df)
                
                st.download_button(
                    label="📥 Κατέβασμα Excel Στατιστικών",
                    data=excel_buffer.getvalue(),
                    file_name="statistika_mathiton.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )
                
        except Exception as e:
            st.error(f"❌ Σφάλμα κατά την επεξεργασία: {str(e)}")
    
    # Show required columns info
    with st.sidebar:
        st.header("📋 Απαιτούμενες Στήλες Excel")
        required_cols = [
            "ΟΝΟΜΑ", "ΦΥΛΟ", "ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ",
            "ΖΩΗΡΟΣ", "ΙΔΙΑΙΤΕΡΟΤΗΤΑ", "ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ", 
            "ΦΙΛΟΙ", "ΣΥΓΚΡΟΥΣΗ", "ΤΜΗΜΑ"
        ]
        for col in required_cols:
            st.text(f"• {col}")
    
    # Show sample data link
    with st.sidebar:
        st.markdown("---")
        st.header("📋 Sample Data")
        st.markdown("""
        **Για δοκιμή της εφαρμογής:**
        
        Μπορείτε να δημιουργήσετε ένα δείγμα Excel με τα παρακάτω δεδομένα:
        
        | ΟΝΟΜΑ | ΦΥΛΟ | ΠΑΙΔΙ_ΕΚΠΑΙΔΕΥΤΙΚΟΥ | ΖΩΗΡΟΣ | ΙΔΙΑΙΤΕΡΟΤΗΤΑ | ΚΑΛΗ_ΓΝΩΣΗ_ΕΛΛΗΝΙΚΩΝ | ΦΙΛΟΙ | ΣΥΓΚΡΟΥΣΗ | ΤΜΗΜΑ |
        |-------|------|-------------------|--------|---------------|-------------------|-------|-----------|-------|
        | Άννα | Κ | Ν | Ν | Ο | Ν | | | Α1 |
        | Γιάννης | Α | Ο | Ν | Ν | Ν | | | Α1 |
        | Μαρία | Κ | Ν | Ο | Ο | Ν | | | Α2 |
        | Πέτρος | Α | Ο | Ν | Ο | Ο | | | Α2 |
        """)
    
    # Additional info
    with st.sidebar:
        st.markdown("---")
        st.header("ℹ️ Πληροφορίες")
        st.markdown("""
        **Έκδοση:** 1.0.0  
        **Τελευταία ενημέρωση:** Αύγουστος 2024  
        **Συμβατότητα:** Excel 2016+  
        
        **Υποστήριξη:**  
        Για ερωτήσεις ή προβλήματα, επικοινωνήστε με τον διαχειριστή.
        """)


def show_terms_page():
    """Εμφανίζει τη σελίδα αποδοχής όρων χρήσης."""
    st.header("📋 Όροι Χρήσης")
    
    st.markdown("""
    **Όροι και Προϋποθέσεις Χρήσης**
    
    Με τη χρήση αυτής της εφαρμογής συμφωνείτε με τα ακόλουθα:
    
    1. **Εμπιστευτικότητα**: Τα δεδομένα μαθητών είναι ευαίσθητα και θα χειριστούν με απόλυτη εμπιστευτικότητα.
    
    2. **Προστασία Δεδομένων**: Η εφαρμογή δεν αποθηκεύει δεδομένα μόνιμα. Όλα τα δεδομένα διαγράφονται μετά τη χρήση.
    
    3. **Νόμιμη Χρήση**: Η εφαρμογή προορίζεται αποκλειστικά για εκπαιδευτικούς σκοπούς.
    
    4. **Πνευματικά Δικαιώματα**: Η εφαρμογή προστατεύεται από πνευματικά δικαιώματα.
    
    5. **Ευθύνη Χρήστη**: Ο χρήστης είναι υπεύθυνος για την ακρίβεια των δεδομένων που εισάγει.
    
    6. **Τεχνική Υποστήριξη**: Η εφαρμογή παρέχεται "ως έχει" χωρίς εγγυήσεις.
    """)
    
    st.markdown("---")
    
    # Warning box
    st.warning("""
    ⚠️ **Σημαντική Υπενθύμιση:**
    
    Τα δεδομένα μαθητών περιέχουν προσωπικές πληροφορίες. Βεβαιωθείτε ότι:
    - Έχετε τη σχετική άδεια για χρήση των δεδομένων
    - Συμμορφώνεστε με το GDPR και τους τοπικούς νόμους
    - Δεν μοιράζεστε τα αποτελέσματα χωρίς άδεια
    """)
    
    st.markdown("---")
    
    # Acceptance buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Αποδέχομαι τους Όρους", type="primary", use_container_width=True):
            st.session_state.terms_accepted = True
            st.success("Όροι εγκρίθηκαν! Ανακατεύθυνση...")
            st.rerun()
    
    with col2:
        if st.button("📖 Διαβάζω ξανά", type="secondary", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("❌ Δεν Αποδέχομαι", type="secondary", use_container_width=True):
            st.error("Δεν μπορείτε να χρησιμοποιήσετε την εφαρμογή χωρίς αποδοχή των όρων.")
            st.stop()


def reset_application():
    """Επανεκκίνηση της εφαρμογής."""
    for key in list(st.session_state.keys()):
        if key != "terms_accepted":
            del st.session_state[key]


if __name__ == "__main__":
    main()
