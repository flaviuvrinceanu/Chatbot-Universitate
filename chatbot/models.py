class Model:
    def generate(self, text):
        import os, re, html
        import torch, platform, sys
        from transformers import StoppingCriteria, StoppingCriteriaList
        from huggingface_hub import login
        import os
        import torch, os
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        from peft import PeftModel

        tok = "-"

        BASE = "meta-llama/Llama-2-7b-chat-hf"
        ADAPTER_DIR = "chatbot/utcn_lora_out"

        bnb = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8 else torch.float16,
        )

        tokenizer = AutoTokenizer.from_pretrained(BASE, use_fast=True, token=tok)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        tokenizer.truncation_side = "right"
        tokenizer.model_max_length = 4096

        base = AutoModelForCausalLM.from_pretrained(
            BASE,
            token=tok,
            device_map="auto",
            quantization_config=bnb,
            trust_remote_code=False
        )

        # model = PeftModel.from_pretrained(base, ADAPTER_DIR, is_trainable=False)
        model = PeftModel.from_pretrained(
            base,                  # base model
            ADAPTER_DIR,           # adapter path (local or HF repo ID)
            is_trainable=False
        )


        model.eval()
        print(" Loaded base + adapters")


        # --- Grounded prompt helpers


        OFFICIAL_URLS = {
            "sinu_portal":    "https://websinu.utcluj.ro/",
            "main_site_en":   "https://www.utcluj.ro/en/",
            "main_site_ro":   "https://www.utcluj.ro/",
            "admission":      "https://admitereonline.utcluj.ro/",
            "digital":        "https://utcluj.digital/",
        }

        WHITELIST_DOMAINS = {
            "utcluj.ro", "websinu.utcluj.ro",
            "admitereonline.utcluj.ro", "utcluj.digital"
        }

        SYSTEM_EN = (
            "You are the UTCN assistant. Answer clearly, correctly, and concisely for students. "
            "Use only the official domains: utcluj.ro, websinu.utcluj.ro, "
            "admitereonline.utcluj.ro, utcluj.digital. "
            "If you are not sure, say you’re not sure. Do not invent URLs or dates. Do not use HTML."
        )
        SYSTEM_RO = (
            "Ești asistentul UTCN. Răspunde clar, corect și concis pentru studenți. "
            "Folosește doar domeniile oficiale: utcluj.ro, websinu.utcluj.ro, "
            "admitereonline.utcluj.ro, utcluj.digital. "
            "Dacă nu ești sigur, spune că nu ești sigur. Nu inventa URL-uri sau date. Nu folosi HTML."
        )

        def grounding_facts(lang: str = "en") -> str:
            if lang.lower().startswith("ro"):
                return (
                    "FAPTE:\n"
                    f"- Portal studenti - SINU (autentificare): {OFFICIAL_URLS['sinu_portal']}\n"
                    f"- Site principal: {OFFICIAL_URLS['main_site_ro']}\n"
                    f"- Admitere: {OFFICIAL_URLS['admission']}\n"
                    f"- UTCluj.Digital: {OFFICIAL_URLS['digital']}\n"
                )
            else:
                return (
                    "FACTS:\n"
                    f"- SINU (login): {OFFICIAL_URLS['sinu_portal']}\n"
                    f"- Main site (EN): {OFFICIAL_URLS['main_site_en']}\n"
                    f"- Admissions: {OFFICIAL_URLS['admission']}\n"
                    f"- UTCluj.Digital: {OFFICIAL_URLS['digital']}\n"
                )


        def build_prompt(user_text: str, lang: str = "en") -> str:
            sys_prompt = SYSTEM_RO if lang.lower().startswith("ro") else SYSTEM_EN
            facts = grounding_facts(lang)
            return f"<<SYS>>{sys_prompt}\n{facts}<</SYS>>\nUser: {user_text}\nAssistant:"


        STOP_STRINGS = ["\nUser:", "\nQuestion:", "<<SYS>>", "[/INST]"]

        class KeywordStopper(StoppingCriteria):
            def __init__(self, keywords, tokenizer):
                self.encoded = [tokenizer.encode(k, add_special_tokens=False) for k in keywords]
            def __call__(self, input_ids, scores, **kwargs):
                seq = input_ids[0].tolist()
                for k in self.encoded:
                    if len(seq) >= len(k) and seq[-len(k):] == k:
                        return True
                return False

        def strip_html(text: str) -> str:
            text = re.sub(r"<[^>]+>", " ", text)
            text = html.unescape(text)
            return re.sub(r"\s+", " ", text).strip()

        @torch.inference_mode()
        def generate(user_text: str, lang: str = "en", max_new_tokens=200, temperature=0.7, top_p=0.9, do_sample=False):
            prompt = build_prompt(user_text, lang=lang)
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

            stopper = StoppingCriteriaList([KeywordStopper(STOP_STRINGS, tokenizer)])

            out = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=1.1,
                eos_token_id=tokenizer.eos_token_id,
                stopping_criteria=stopper,
            )
            full = tokenizer.decode(out[0], skip_special_tokens=True)
            ans = full.split("Assistant:", 1)[-1] if "Assistant:" in full else full
            for s in STOP_STRINGS:
                if s in ans:
                    ans = ans.split(s, 1)[0]
            return strip_html(ans).strip()

        print("Helpers ready. Call generate('Your question', lang='en'|'ro')")

        return generate(text)

# print(generate("Where do I log in to the student portal?", lang="en"))
# print("---")
# print(generate("Unde mă autentific în portalul studenților ?", lang="ro"))
