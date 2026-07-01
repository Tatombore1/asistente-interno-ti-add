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

st.set_page_config(
    page_title="Asistente Interno de TI ADD",
    page_icon=":material/support_agent:",
    layout="centered",
)


@st.cache_resource(show_spinner="Procesando el manual de soporte...")
def build_agent(api_key: str) -> SupportAgent:
    chunks = load_pdf(PDF_PATH)
    embed_model = os.getenv("COHERE_EMBED_MODEL", "embed-v4.0")
    chat_model = os.getenv("COHERE_CHAT_MODEL", "command-a-plus-05-2026")
    retriever = CohereRetriever(api_key, chunks, embed_model)
    return SupportAgent(api_key, retriever, chat_model)


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
selected_example = st.selectbox(
    "Pregunta de ejemplo", ["Selecciona una pregunta..."] + examples
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Escribe una consulta operativa para el Area de TI")
if selected_example != "Selecciona una pregunta...":
    question = selected_example

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
