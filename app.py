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

# PDF served from Streamlit static folder
PDF_URL = "static/Gambit_Chess_Article.pdf"

# Open PDF in new tab (Chrome-safe)
st.markdown(
    f"""
    <p style="padding-top:10px; font-size:20px;">
        <a href="{PDF_URL}" target="_blank" style="text-decoration:none;">
        📄 Open PDF article in a new tab
        </a>
    </p>
    """,
    unsafe_allow_html=True
)

# Optional download button
try:
    with open("static/Gambit_Chess_Article.pdf", "rb") as f:
        st.download_button(
            label="⬇️ Download PDF article",
            data=f,
            file_name="Gambit_Chess_Article.pdf",
            mime="application/pdf"
        )
except FileNotFoundError:
    st.error("❌ PDF not found in /static/. Please ensure it is uploaded correctly.")

# ------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------

