import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.agent import SupportAgent
from src.document_loader import load_pdfs
from src.retriever import CohereRetriever


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
LOGO_SQUARE_PATH = BASE_DIR / "assets" / "add-logo-square.svg"
LOGO_BANNER_PATH = BASE_DIR / "assets" / "add-logo-banner.svg"

PRIMARY_DOCUMENTS = [
    DATA_DIR / "casos_operativos_soporte_ti_add.pdf",
    DATA_DIR / "herramientas_y_administracion_ti_add.pdf",
]
EXAMPLES = [
    "¿Como verifico el numero de serie de una notebook?",
    "Un usuario no puede conectarse por VPN. ¿Que pasos sigo?",
    "Un usuario se olvido la contraseña de su correo. ¿Cuales son los pasos?",
]

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


def _ensure_dirs() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def _document_paths() -> list[Path]:
    paths = list(PRIMARY_DOCUMENTS)
    paths.extend(sorted(UPLOADS_DIR.glob("*.pdf")))
    return [path for path in paths if path.exists()]


def _save_uploaded_file(uploaded_file) -> Path:
    target = UPLOADS_DIR / uploaded_file.name
    target.write_bytes(uploaded_file.getbuffer())
    return target


def _delete_uploaded_file(path: Path) -> None:
    if path.exists():
        path.unlink()


@st.cache_resource(show_spinner="Procesando la base documental...")
def build_agent(api_key: str, document_paths: tuple[str, ...]) -> SupportAgent:
    chunks = load_pdfs([Path(path) for path in document_paths])
    embed_model = os.getenv("COHERE_EMBED_MODEL", "embed-v4.0")
    chat_model = os.getenv("COHERE_CHAT_MODEL", "command-a-plus-05-2026")
    retriever = CohereRetriever(api_key, chunks, embed_model)
    return SupportAgent(api_key, retriever, chat_model)


_ensure_dirs()

st.image(str(LOGO_BANNER_PATH), use_container_width=True)
st.title("Asistente Interno de TI ADD")
st.caption(
    "Consultas operativas para el equipo de soporte TI de Distribuidora ADD"
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
    current_paths = _document_paths()

    st.subheader("Base documental activa")
    st.caption(
        "La IA consulta todos los documentos operativos cargados actualmente "
        "para asistir al Area de TI."
    )

    for primary_document in PRIMARY_DOCUMENTS:
        if not primary_document.exists():
            continue
        st.download_button(
            f"Descargar {primary_document.name}",
            data=primary_document.read_bytes(),
            file_name=primary_document.name,
            mime="application/pdf",
            use_container_width=True,
        )

    st.divider()
    st.subheader("Gestion de archivos")
    uploaded_file = st.file_uploader(
        "Agregar o reemplazar PDF en la base",
        type=["pdf"],
        key="uploader-base-general",
        help="Si subes un archivo con el mismo nombre que uno ya cargado, se reemplaza.",
    )
    if uploaded_file is not None and st.button(
        "Guardar archivo",
        key="save-upload-base-general",
        use_container_width=True,
    ):
        saved_path = _save_uploaded_file(uploaded_file)
        build_agent.clear()
        st.success(f"Archivo guardado: {saved_path.name}")
        st.rerun()

    st.caption("Documentos que usa actualmente la IA:")
    for path in current_paths:
        label = "Principal" if path in PRIMARY_DOCUMENTS else "Extra"
        st.write(f"- {label}: {path.name}")

    extra_documents = [path for path in current_paths if path not in PRIMARY_DOCUMENTS]
    if extra_documents:
        st.divider()
        st.subheader("Eliminar documentos extra")
        removable_document = st.selectbox(
            "Selecciona un PDF cargado manualmente",
            [path.name for path in extra_documents],
            key="removable_document",
        )
        if st.button("Eliminar PDF seleccionado", use_container_width=True):
            target = UPLOADS_DIR / removable_document
            _delete_uploaded_file(target)
            build_agent.clear()
            st.success(f"Archivo eliminado: {removable_document}")
            st.rerun()

    st.divider()
    st.caption(
        "El asistente responde solo con informacion contenida en los documentos "
        "cargados actualmente."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_example_used" not in st.session_state:
    st.session_state.last_example_used = None

messages = st.session_state.messages
last_example_used = st.session_state.last_example_used
example_placeholder = "Selecciona una pregunta..."

selected_example = st.selectbox(
    "Pregunta de ejemplo",
    [example_placeholder] + EXAMPLES,
    key="selected_example_global",
)

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Describe el caso y pregunta que deberia hacer soporte")
if (
    not question
    and selected_example != example_placeholder
    and selected_example != last_example_used
):
    question = selected_example
    st.session_state.last_example_used = selected_example

if question:
    messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        document_paths = tuple(str(path) for path in _document_paths())
        agent = build_agent(api_key, document_paths)
        with st.chat_message("assistant"):
            with st.spinner("Buscando en la base documental..."):
                response = agent.ask(question)
            st.markdown(response.answer)
            with st.expander("Ver fragmentos consultados"):
                for source in response.sources:
                    st.markdown(
                        f"**Pagina {source.chunk.page}** "
                        f"(similitud: {source.score:.2f}) "
                        f"- `{source.chunk.source}`"
                    )
                    st.write(source.chunk.text)
        messages.append({"role": "assistant", "content": response.answer})
    except Exception as error:
        st.error(f"No fue posible responder: {error}")
