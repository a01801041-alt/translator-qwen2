"""
Translator App using Qwen2-0.5B
Translates text between multiple languages without any external API keys.
"""

import gradio as gr
from translator import Translator

# Supported languages
LANGUAGES = {
    "English": "English",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Italian": "Italian",
    "Portuguese": "Portuguese",
    "Chinese": "Chinese",
    "Japanese": "Japanese",
    "Arabic": "Arabic",
    "Russian": "Russian",
}

# Initialize translator (loaded once)
print("Loading Qwen2-0.5B model... This may take a moment.")
translator = Translator()
print("Model loaded successfully!")


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text from source language to target language."""
    if not text.strip():
        return "⚠️ Please enter text to translate."
    if source_lang == target_lang:
        return "⚠️ Source and target languages must be different."
    return translator.translate(text, source_lang, target_lang)


def build_ui():
    with gr.Blocks(
        title="Translator — Qwen2-0.5B",
        theme=gr.themes.Soft(),
        css="""
        .title { text-align: center; margin-bottom: 8px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 24px; }
        """,
    ) as demo:
        gr.Markdown("# 🌐 Translator App", elem_classes="title")
        gr.Markdown(
            "Powered by **Qwen2-0.5B** — no API keys required, runs 100% locally.",
            elem_classes="subtitle",
        )

        with gr.Row():
            with gr.Column():
                source_lang = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    value="English",
                    label="Source Language",
                )
                input_text = gr.Textbox(
                    lines=6,
                    placeholder="Enter text to translate...",
                    label="Input Text",
                )
            with gr.Column():
                target_lang = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    value="Spanish",
                    label="Target Language",
                )
                output_text = gr.Textbox(
                    lines=6,
                    label="Translation",
                    interactive=False,
                )

        translate_btn = gr.Button("🔄 Translate", variant="primary", size="lg")

        # Example phrases
        gr.Markdown("### 💡 Example Phrases")
        gr.Examples(
            examples=[
                ["I like soccer", "English", "Spanish"],
                ["How are you?", "English", "Spanish"],
                ["What time is it?", "English", "Spanish"],
                ["I like soccer", "English", "French"],
                ["How are you?", "English", "German"],
                ["What time is it?", "English", "Portuguese"],
            ],
            inputs=[input_text, source_lang, target_lang],
        )

        translate_btn.click(
            fn=translate_text,
            inputs=[input_text, source_lang, target_lang],
            outputs=output_text,
        )
        # Also translate on Enter (submit)
        input_text.submit(
            fn=translate_text,
            inputs=[input_text, source_lang, target_lang],
            outputs=output_text,
        )

    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch(share=False, server_name="0.0.0.0", server_port=7860)
