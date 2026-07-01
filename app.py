import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.agent import SupportAgent
from src.document_loader import load_pdf
from src.retriever import CohereRetriever


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "data" / "procedimientos_y_guias_soporte_ti_distribuidora_add.pdf"
LOGO_SQUARE_PATH = BASE_DIR / "assets" / "add-logo-square.svg"
LOGO_BANNER_PATH = BASE_DIR / "assets" / "add-logo-banner.svg"

st.set_page_config(
    page_title="Asistente Interno de TI ADD",
    page_icon=":material/support_agent:",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --add-red: #ef3b2d;
        --add-orange: #ff9800;
        --add-ink: #172033;
        --add-muted: #5b6474;
        --add-surface: #fffaf7;
        --add-line: #ece5df;
    }

    .stApp {
        background: #ffffff;
        color: var(--add-ink);
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.96);
        border-bottom: 1px solid var(--add-line);
    }

    [data-testid="stSidebar"] {
        background: #fffaf7;
        border-right: 1px solid var(--add-line);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    h1, h2, h3, p, label, div {
        color: var(--add-ink);
    }

    .stCaption {
        color: var(--add-muted);
    }

    [data-testid="stChatInput"] {
        background: #ffffff;
    }

    [data-testid="stChatInput"] textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput input {
        background: #fff;
        border: 1px solid var(--add-line);
        border-radius: 16px;
    }

    [data-testid="stChatInput"] > div {
        background: #ffffff;
        border-top: 1px solid var(--add-line);
    }

    .stButton > button,
    .stDownloadButton > button {
        background: var(--add-red);
        color: #fff;
        border: none;
        border-radius: 999px;
        font-weight: 700;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #d83427;
        color: #fff;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--add-line);
        border-radius: 18px;
        background: #ffffff;
    }

    [data-testid="stChatMessage"] {
        background: #ffffff;
        border: 1px solid var(--add-line);
        border-radius: 20px;
        padding: 0.35rem;
    }

    [data-testid="stChatMessageContent"] p {
        color: var(--add-ink);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Procesando el manual de soporte...")
def build_agent(api_key: str) -> SupportAgent:
    chunks = load_pdf(PDF_PATH)
    embed_model = os.getenv("COHERE_EMBED_MODEL", "embed-v4.0")
    chat_model = os.getenv("COHERE_CHAT_MODEL", "command-a-plus-05-2026")
    retriever = CohereRetriever(api_key, chunks, embed_model)
    return SupportAgent(api_key, retriever, chat_model)


st.image(str(LOGO_BANNER_PATH), use_container_width=True)
st.title("Asistente Interno de TI ADD")
st.caption(
    "Consultas para el equipo de soporte basadas en el documento "
    "Procedimientos y Guias de Soporte TI de Distribuidora ADD"
)

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    st.warning(
        "Configura COHERE_API_KEY en el archivo .env o como variable de entorno "
        "para comenzar."
    )
    st.stop()

with st.sidebar:
    st.image(str(LOGO_SQUARE_PATH), use_container_width=True)
    st.subheader("Documento consultado")
    st.write("Procedimientos y Guias de Soporte TI - Distribuidora ADD")
    st.download_button(
        "Descargar manual",
        data=PDF_PATH.read_bytes(),
        file_name=PDF_PATH.name,
        mime="application/pdf",
        use_container_width=True,
    )
    st.divider()
    st.caption(
        "El asistente responde solo con informacion contenida en el manual "
        "interno del Area de TI."
    )

examples = [
    "¿Que hago si olvide mi contraseña del correo?",
    "¿En cuanto tiempo atienden un incidente critico?",
    "¿Que hago si olvide mi contraseña del SGI?",
    "¿Como abro un ticket en la plataforma interna?",
    "¿Que revisar si un usuario no abre su carpeta compartida?",
    "¿Que revisar si no funciona una impresora?",
    "¿Como verifico el numero de serie de una notebook?",
    "¿Como conectarse a Exchange Online desde PowerShell?",
]
EXAMPLE_PLACEHOLDER = "Selecciona una pregunta..."
selected_example = st.selectbox(
    "Pregunta de ejemplo",
    [EXAMPLE_PLACEHOLDER] + examples,
    key="selected_example",
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_example_used" not in st.session_state:
    st.session_state.last_example_used = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Escribe una consulta operativa para el Area de TI")
if (
    not question
    and selected_example != EXAMPLE_PLACEHOLDER
    and selected_example != st.session_state.last_example_used
):
    question = selected_example
    st.session_state.last_example_used = selected_example

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        agent = build_agent(api_key)
        with st.chat_message("assistant"):
            with st.spinner("Buscando en el manual..."):
                response = agent.ask(question)
            st.markdown(response.answer)
            with st.expander("Ver fragmentos consultados"):
                for source in response.sources:
                    st.markdown(
                        f"**Pagina {source.chunk.page}** "
                        f"(similitud: {source.score:.2f})"
                    )
                    st.write(source.chunk.text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response.answer}
        )
    except Exception as error:
        st.error(f"No fue posible responder: {error}")
