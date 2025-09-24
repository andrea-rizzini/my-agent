import os, httpx

async def generate_reply(system_prompt: str, user_input: str, temperature: float, top_p: float) -> str:
    backend = os.getenv("BACKEND", "echo")  # echo|ollama
    if backend == "echo":
        return f"[echo] {user_input}"

    if backend == "ollama":
        model = os.getenv("MODEL_ID", "llama3")
        # Request to Ollama (http://localhost:11434)
        payload = {
            "model": model,
            "system": system_prompt,
            "prompt": user_input,
            "stream": False,
            "options": {"temperature": temperature, "top_p": top_p}
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post("http://localhost:11434/api/generate", json=payload)
            r.raise_for_status()
            return r.json().get("response","")
    raise RuntimeError("BACKEND sconosciuto")