import os
import openai

openai.api_key = os.getenv("")

def suggest_selector(html_sample, target_text):
    prompt = f"""
    Tengo este fragmento HTML:
    {html_sample}
    ¿Cuál sería un selector CSS robusto para capturar el elemento que contiene: {target_text}?
    Devuelve solo el selector CSS.
    """
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120
    )
    selector = res.choices[0].message["content"].strip()
    return selector
