import streamlit as st
import base64

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Lichess Opening Explorer + Chess Article",
    layout="wide"
)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
st.sidebar.title("Database & Filters")

# Database selector
db_choice = st.sidebar.radio(
    "Database",
    ["Lichess (online games)", "Masters (OTB)"],
    index=0
)

# Game speeds (for Lichess only)
if db_choice == "Lichess (online games)":
    st.sidebar.subheader("Game speeds (online)")
    speeds = st.sidebar.multiselect(
        "Speeds",
        ["bullet", "blitz", "rapid", "classical"],
        default=["blitz", "rapid", "classical"]
    )
else:
    speeds = []

# Rating filters (for Lichess only)
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
(online or Masters database) to see the most common next moves and their statistics.
""")

# ------------------------------------------------------------
# FEN INPUT
# ------------------------------------------------------------
fen_input = st.text_input(
    "FEN position",
    value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

# ------------------------------------------------------------
# QUERY BUTTON (placeholder)
# ------------------------------------------------------------
if st.button("Query Lichess"):
    st.info("⚙️ Lichess API query would run here (your existing logic).")
    st.write("FEN queried:", fen_input)

# ------------------------------------------------------------
# PDF ARTICLE SECTION
# ------------------------------------------------------------
st.write("---")
st.subheader("📘 View the Chess Article")

PDF_FILE = "Gambit_Chess_Article.pdf"

if st.button("📄 View PDF article"):
    try:
        with open(PDF_FILE, "rb") as f:
            pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        # Embedded PDF viewer
        pdf_display = f"""
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" 
                height="1100" 
                type="application/pdf">
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"❌ PDF file '{PDF_FILE}' not found.")
        st.info("Make sure the PDF is in the same folder as app.py.")

    except Exception as e:
        st.error(f"❌ Error loading PDF: {e}")
        st.info("If the PDF is large, use a link-to-open method instead.")

# ------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------
