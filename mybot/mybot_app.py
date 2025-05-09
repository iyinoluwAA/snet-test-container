# Frontend with Gradio

"""
This python file defines the UI components, dynamic model selector, and ties into process_message.
"""
import os
import gradio as gr
from dotenv import load_dotenv
from mybot_template import process_message

# Load env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Available models
AVAILABLE_MODELS = [
    os.getenv("REPLICATE_MODEL", "meta/meta-llama-3-70b"),
    "ibm-granite/granite-3.3-8b-instruct"
]

def launch_app():
    with gr.Blocks(title="🎛 Custom Chatbot") as demo:
        gr.Markdown("# 🚀 Customizable AI Chatbot")

        # Model selector
        with gr.Row():
            model_selector = gr.Dropdown(
                choices=AVAILABLE_MODELS,
                value=AVAILABLE_MODELS[0],
                label="Select Replicate Model",
                interactive=True
            )

        # Chat window
        with gr.Row():
            chatbot = gr.Chatbot(
                label="Chat Window",
                height=400, 
                type="messages"
                )

        # User input
        with gr.Row():
            user_input = gr.Textbox(
                label="Your Message",
                placeholder="Type your message and hit Enter..."
            )

        # Advanced accordion
        with gr.Accordion("⚙️ Advanced Settings", open=False):
            gr.Markdown(
                """
                - Change `temperature`, `max_tokens`, etc. in `bot_template.py` or expose sliders here.
                - Add more models by editing `AVAILABLE_MODELS` above.
                - Monitor logs in your terminal for real‑time debugging.
                """
            )
        
        # Thought stream display
        think_display = gr.Markdown(label="Thought Process")

        # Clear button
        clear_btn = gr.ClearButton([user_input, chatbot, think_display])

        # Bind submit
        user_input.submit(
            fn=process_message,
            inputs=[chatbot, user_input, model_selector],
            outputs=[chatbot, think_display, user_input],
            show_progress="full"
        )

    demo.launch(server_name="0.0.0.0", server_port=7865)

if __name__ == "__main__":
    launch_app()
