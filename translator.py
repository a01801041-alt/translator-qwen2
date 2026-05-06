"""
Translator module — wraps Qwen2-0.5B (via HuggingFace Transformers)
to perform text translation between multiple languages.
"""

from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2-0.5B-Instruct"

SYSTEM_PROMPT = (
    "You are a professional translator. "
    "When given a translation task, you respond ONLY with the translated text — "
    "no explanations, no notes, no punctuation changes beyond what the target language requires. "
    "Never add extra sentences or commentary."
)


class Translator:
    """Loads Qwen2-0.5B-Instruct once and exposes a translate() method."""

    def __init__(self, model_id: str = MODEL_ID) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
        )
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        self.model.eval()

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate *text* from *source_lang* into *target_lang*.

        Returns the translated string, or an error message prefixed with '❌'.
        """
        user_message = (
            f"Translate the following {source_lang} text into {target_lang}. "
            f"Reply with ONLY the translation, nothing else.\n\n"
            f"Text: {text}"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        # Build prompt using the chat template
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,          # greedy — deterministic & faster
                temperature=None,
                top_p=None,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Decode only the newly generated tokens
        new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
        result = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        return result if result else "❌ Model returned an empty response. Please try again."
