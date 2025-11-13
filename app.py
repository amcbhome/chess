import streamlit as st

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

# Rating filters
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
(online or Masters DB) to see the most common next moves and their statistics.
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
# PDF ARTICLE SECTION (STATIC FILE)
# ------------------------------------------------------------
st.write("---")
st.subheader("📘 View the Chess Article")

PDF_URL = "static/Gambit_Chess_Article.pdf"

# Open in a new tab (Chrome-compatible)
st.markdown(
    f"""
    <div style="padding-bottom:15px;">
        <a href="{PDF_URL}" target="_blank"
           style="font-size:20px; text-decoration:none;">
           📄 Open PDF article in a new tab
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Optional download button
try:
    with open(f".streamlit/{PDF_URL}", "rb") as f:
        st.download_button(
            label="⬇️ Download PDF article",
            data=f,
            file_name="Gambit_Chess_Article.pdf",
            mime="application/pdf"
        )
except Exception:
    st.info(
        "If the download fails, ensure the PDF is in `.streamlit/static/`."
    )

# ------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------

