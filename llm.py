# llm.py
import panel as pn
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
    instructions="Eres VisAI, un asistente para resolver dudas sobre los datos financieros de Visa Group. Responde de manera clara y concisa."
)

async def response_callback(input_message: str, instance: pn.chat.ChatInterface):
    """Callback function for processing chat messages"""
    try:
        response = await visa_agent.run(input_message)
        return response.output
    except Exception as e:
        return f"Error: {str(e)}"

# Define the custom stylesheet
custom_message_stylesheet = """
.message {
    font-size: 1.1em; */
}
"""

# Create the chat UI with bigger input and custom buttons
chat_ui = pn.chat.ChatInterface(
    callback=response_callback,
    header=pn.pane.Markdown("# Asistente VisAI"),
    user="Usuario",
    avatar="🧑‍💻",
    callback_user="VisAI 🤖",
    widgets=pn.chat.ChatAreaInput(
        placeholder="Escribe aquí...",
        height=120,  # Made bigger as requested
        sizing_mode="stretch_width"
    ),
    show_undo=False,
    show_rerun=False,
    show_button_name=False,
    sizing_mode="stretch_width",
    # Add message_params to apply the stylesheet to chat messages
    message_params={"stylesheets": [custom_message_stylesheet]}
)