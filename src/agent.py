from src.models import AgentResponse, SearchResult
from src.retriever import CohereRetriever


SYSTEM_PROMPT = """Eres un asistente interno para el equipo de soporte TI de Distribuidora ADD.
Ayudas principalmente a analistas y personal del Area de TI a consultar procedimientos operativos.
Responde exclusivamente con la informacion de los fragmentos recuperados del manual.
Si la respuesta no aparece en el contexto, indica claramente que no esta documentada.
No inventes procedimientos, contactos, plazos ni permisos.
Responde en espanol, de forma clara y practica.
Incluye referencias entre corchetes con el formato [pagina N]."""


class SupportAgent:
    def __init__(
        self,
        api_key: str,
        retriever: CohereRetriever,
        chat_model: str = "command-a-plus-05-2026",
    ) -> None:
        import cohere

        self.client = cohere.ClientV2(api_key=api_key)
        self.retriever = retriever
        self.chat_model = chat_model

    @staticmethod
    def _context(results: list[SearchResult]) -> str:
        return "\n\n".join(
            f"FUENTE {index} - pagina {result.chunk.page}:\n{result.chunk.text}"
            for index, result in enumerate(results, start=1)
        )

    def ask(self, question: str) -> AgentResponse:
        results = self.retriever.search(question)
        prompt = (
            f"CONTEXTO DEL MANUAL:\n{self._context(results)}\n\n"
            f"PREGUNTA DEL USUARIO:\n{question}"
        )
        response = self.client.chat(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        answer_parts = [
            item.text
            for item in response.message.content
            if getattr(item, "type", None) == "text" and getattr(item, "text", None)
        ]
        if not answer_parts:
            raise ValueError("Cohere no devolvio una respuesta de texto")
        answer = "\n".join(answer_parts)
        return AgentResponse(answer=answer, sources=results)
