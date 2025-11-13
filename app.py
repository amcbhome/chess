import streamlit as st
import base64

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Lichess Opening Explorer + Article Viewer",
    layout="wide"
)

# ------------------------------------------------------------
# SIDEBAR: DATABASE & FILTERS
# ------------------------------------------------------------
st.sidebar.title("Database & Filters")

# Database selector
db_choice = st.sidebar.radio(
    "Database",
    ["Lichess (online games)", "Masters (OTB)"],
    index=0
)

# Game speeds (only for Lichess)
if db_choice == "Lichess (online games)":
    st.sidebar.subheader("Game speeds (online)")
    speeds = st.sidebar.multiselect(
        "Speeds",
        ["bullet", "blitz", "rapid", "classical"],
        default=["blitz", "rapid", "classical"]
    )
else:
    speeds = []

# Rating filters (only for Lichess)
if db_choice == "Lichess (online games)":
    st.sidebar.subheader("Rating filters (online)")
    rating_bucket = st.sidebar.selectbox(
        "Rating buckets",
        ["All ratings", "0-900", "900-1200", "1200-1500",
         "1500-1800", "1800-2100", "2100+"],
        index=0
    )

st.sidebar.write("---")
st.sidebar.write("Filters ready.")

# ------------------------------------------------------------
# MAIN TITLE
# ------------------------------------------------------------
st.title("♟️ Lichess Opening Statistics from FEN")

st.write("""
Enter any chess position in **FEN format** and query the Lichess Opening Explorer
(online or Masters DB) to find the most common next moves and their statistics.
""")

# ------------------------------------------------------------
# FEN INPUT
# ------------------------------------------------------------
fen_input = st.text_input(
    "FEN position",
    value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

# ------------------------------------------------------------
# QUERY BUTTON (placeholder for your existing code)
# ------------------------------------------------------------
if st.button("Query Lichess"):
    st.info("⚙️ Lichess API query would run here (your existing logic).")
    st.write("FEN queried:", fen_input)

# ------------------------------------------------------------
# VIEW PDF ARTICLE SECTION
# ------------------------------------------------------------
st.write("---")
st.subheader("📘 View the Chess Article")

PDF_FILE = "Chess_Article_on_Gambit_Openings.pdf"

if st.button("📄 View PDF article"):
    try:
        with open(PDF_FILE, "rb") as f:
            pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        pdf_display = f"""
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" 
                height="1100" 
                type="application/pdf">
            </iframe>
        """

        st.markdown(pdf_display, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error loading PDF: {e}")
        st.info("Make sure the file is in the same folder as app.py.")

# ------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------
