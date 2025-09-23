import panel as pn
# from panel.chat import ChatInterface
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

ollama_model = OpenAIChatModel(
    model_name="llama3.1",
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

visa_agent = Agent(
    name="Agente VisAI",
    model=ollama_model,
    instructions="Eres VisAI, un asistente para resolver dudas"
)

async def response_callback(input_message: str, instance: pn.chat.ChatInterface):
    response = await visa_agent.run(input_message)
    return response.output

chat_ui = pn.chat.ChatInterface(
    callback=response_callback,
    header=pn.pane.Markdown("# Asistente VisAI"),
    user="Usuario",
    avatar="🧑‍💻",
    callback_user="VisAI 🤖",
    widgets=pn.chat.ChatAreaInput(
        placeholder="Escribe aquí...",
        height=100,
        sizing_mode="stretch_width"
    ),
    show_undo=False,
    show_rerun=False,
    show_button_name=False,
)