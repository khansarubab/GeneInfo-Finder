import streamlit as st
import requests
from deep_translator import GoogleTranslator
# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="GeneInfo Finder",
    layout="centered"
)

# ================= CSS (NO EXTRA SPACE, SINGLE BOX + BLUE SKY) =================
st.markdown("""
<style>

/* REMOVE STREAMLIT DEFAULT GAPS */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* FULL PAGE BACKGROUND */
body {
    background-color: #87CEEB; /* Sky blue */
}

/* MAIN APP BOX */
.app-box {
    max-width: 900px;
    margin: 20px auto;
    background: #f5f9ff;
    padding: 28px 36px;
    border-radius: 20px;
    box-shadow: 0px 14px 34px rgba(0,0,0,0.15);
}

/* TOP BAR */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

/* TITLE */
.title-main {
    font-size: 32px;
    font-weight: 800;
    color: #000080;
    text-align: center;
}
.title-sub {
    font-size: 22px;
    font-weight: 600;
    color: #000000;
    text-align: center;
    margin-bottom: 4px;
}
.title-desc {
    font-size: 16px;
    color: #000000;
    text-align: center;
    margin-bottom: 20px;
}

/* CARDS */
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 18px;
    box-shadow: 0px 5px 12px rgba(0,0,0,0.08);
}

/* BUTTON */
.stButton button {
    background-color: #1f6fe5;
    color: white;
    border-radius: 8px;
    padding: 0.6em 1.5em;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ================= LANGUAGE SYSTEM =================
LANG = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "Hindi": "hi",
    "Spanish": "es"
}

# ================= APP START =================
st.markdown('<div class="app-box">', unsafe_allow_html=True)

# ---- TOP BAR (TITLE + LANGUAGE) ----
st.markdown('<div class="title-main">DNA Glossary – Advanced Encyclopedia</div>', unsafe_allow_html=True)
st.markdown('<div class="title-sub">GeneInfo Finder - Comprehensive Gene Data Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="title-desc">Explore genes, variants, and genomic insights instantly</div>', unsafe_allow_html=True)

# Language selection
col1, col2 = st.columns([3,1])
with col2:
    selected_lang = st.selectbox("🌍 Language", LANG.keys(), label_visibility="collapsed")

lang_code = LANG[selected_lang]

def tr(text):
    if lang_code == "en":
        return text
    try:
        return GoogleTranslator(source="auto", target=lang_code).translate(text)
    except:
        return text

# ================= INPUT CARD =================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(tr("Gene Search"))
gene = st.text_input(tr("Enter Gene Name (e.g. BRCA1)"))
organism = st.selectbox(tr("Select Organism"), ["Homo sapiens", "Mus musculus"])
search = st.button(tr("Analyze Gene"))
st.markdown('</div>', unsafe_allow_html=True)

# ================= SEARCH LOGIC =================
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

        if ids:
            gid = ids[0]
            data = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                params={"db": "gene", "id": gid, "retmode": "json"}
            ).json()["result"][gid]

            # BASIC INFO
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Basic Information"))
            st.write(tr("Gene Name"), ":", data["name"])
            st.write(tr("Gene ID"), ":", data["uid"])
            st.write(tr("Organism"), ":", data["organism"]["scientificname"])
            st.write(tr("Chromosome"), ":", data.get("chromosome"))
            st.write(tr("Location"), ":", data.get("maplocation"))
            st.markdown('</div>', unsafe_allow_html=True)

            # DESCRIPTION
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Gene Description"))
            st.write(tr(data.get("description", "Not available")))
            st.markdown('</div>', unsafe_allow_html=True)

            # FUNCTION
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Biological Function"))
            st.write(tr(data.get("summary", "Not available")))
            st.markdown('</div>', unsafe_allow_html=True)

            # PROTEIN
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(tr("Protein Information"))
            st.markdown(f"[🔗 {tr('View on UniProt')}](https://www.uniprot.org/uniprotkb?query={gene})")
            st.markdown('</div>', unsafe_allow_html=True)

            # PDF DOWNLOAD
            st.markdown('<div class="card">', unsafe_allow_html=True)
            if st.button(tr("Download Gene Report (PDF)")):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 8, f"""
Gene Name: {data['name']}
Gene ID: {data['uid']}
Organism: {data['organism']['scientificname']}
Chromosome: {data.get('chromosome')}
Location: {data.get('maplocation')}

Description:
{data.get('description')}

Function:
{data.get('summary')}
""")
                file = f"{gene}_Gene_Report.pdf"
                pdf.output(file)

                with open(file, "rb") as f:
                    st.download_button(
                        tr("Click to Download PDF"),
                        f,
                        file_name=file,
                        mime="application/pdf"
                    )
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error(tr("Gene not found"))

st.markdown('</div>', unsafe_allow_html=True)
