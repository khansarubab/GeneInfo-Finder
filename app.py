import streamlit as st
import requests
from deep_translator import GoogleTranslator

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="GeneInfo Finder by Khansa – AI Gene Information Tool",
    page_icon="🧬",
    layout="centered"
)

# ================= META DESCRIPTION =================
st.markdown("""
<meta name="description" content="GeneInfo Finder by Khansa is an AI-powered Streamlit app to explore gene information, biological functions, chromosome location, and protein data.">
""", unsafe_allow_html=True)

# ================= STYLING (SKY BLUE ONLY) =================
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding: 2rem 3rem;
}

.hero {
    background: linear-gradient(90deg, #87CEEB, #5dade2);
    padding: 50px;
    border-radius: 22px;
    color: #003366;
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
}

.hero p {
    font-size: 18px;
}

.app-title {
    text-align: center;
    margin-bottom: 30px;
}

.app-title h2 {
    font-size: 30px;
    font-weight: 700;
    color: #2e86c1;
}

.app-title p {
    font-size: 16px;
    opacity: 0.85;
}

.card {
    background: #f4faff;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.10);
    margin-bottom: 22px;
}

.stButton button {
    background: linear-gradient(90deg, #5dade2, #3498db);
    color: white;
    font-size: 16px;
    font-weight: 600;
    border-radius: 10px;
    padding: 10px 26px;
    border: none;
}

.stButton button:hover {
    background: linear-gradient(90deg, #3498db, #2e86c1);
}
</style>
""", unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="hero">
    <h1>🧬 GeneInfo Finder</h1>
    <p>Comprehensive Gene Data Explorer</p>
</div>
""", unsafe_allow_html=True)

# ================= TITLE BELOW HERO =================
st.markdown("""
<div class="app-title">
    <h2>DNA Glossary – Advanced Encyclopedia</h2>
    <p><strong>GeneInfo Finder</strong> – Comprehensive Gene Data Explorer</p>
    <p>Explore genes, variants, and genomic insights instantly</p>
</div>
""", unsafe_allow_html=True)

# ================= LANGUAGE =================
LANG = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "Hindi": "hi",
    "Spanish": "es"
}

selected_lang = st.selectbox("🌍 Language", LANG.keys())
lang_code = LANG[selected_lang]

def tr(text):
    if lang_code == "en":
        return text
    try:
        return GoogleTranslator(source="auto", target=lang_code).translate(text)
    except:
        return text

# ================= INPUT =================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(tr("Gene Search"))
gene = st.text_input(tr("Enter Gene Name (e.g. BRCA1)"))
organism = st.selectbox(tr("Select Organism"), ["Homo sapiens", "Mus musculus"])
search = st.button(tr("Analyze Gene"))
st.markdown('</div>', unsafe_allow_html=True)

# ================= OUTPUT =================
if search and gene.strip():
    with st.spinner(tr("Fetching gene information...")):

        r = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params={
                "db": "gene",
                "term": f"{gene}[Gene Name] AND {organism}[Organism]",
                "retmode": "json"
            }
        ).json()

        ids = r["esearchresult"]["idlist"]

        if not ids:
            st.error(tr("Gene not found"))
        else:
            gid = ids[0]
            data = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                params={
                    "db": "gene",
                    "id": gid,
                    "retmode": "json"
                }
            ).json()["result"][gid]

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Basic Information"))
            st.write("**Gene Name:**", data["name"])
            st.write("**Gene ID:**", data["uid"])
            st.write("**Organism:**", data["organism"]["scientificname"])
            st.write("**Chromosome:**", data.get("chromosome"))
            st.write("**Location:**", data.get("maplocation"))
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Gene Description"))
            st.write(tr(data.get("description", "Not available")))
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Biological Function"))
            st.write(tr(data.get("summary", "Not available")))
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Protein Information"))
            st.markdown(
                f"[View on UniProt](https://www.uniprot.org/uniprotkb?query={gene})"
            )
            st.markdown('</div>', unsafe_allow_html=True)
