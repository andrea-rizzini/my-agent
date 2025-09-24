import json, hashlib, time, os

def canon(o) -> bytes:
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def build_manifest():
    # --- CORE: cambia raramente ---
    core = {
        "model": {
            # se usi Ollama: es. "llama3:8b"
            "id": os.getenv("MODEL_ID", "echo-backend"),
            "provider": os.getenv("BACKEND", "echo")  # echo|ollama
        },
        "adapters": []
    }

    # --- PROFILE: medio variabile ---
    with open("prompts/system.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    profile = {
        "system_prompt_sha256": sha256(system_prompt.encode("utf-8")),
        "tools_schema_sha256": sha256(json.dumps({
            "tools":[
                {"name":"echo","desc":"Ribalta/ritrasmette il testo.","schema":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}}
            ]
        }, sort_keys=True).encode()),
        "decode_defaults": {"temperature": 0.2, "top_p": 0.9},
        "rag": {"sources":[]}
    }

    # --- STATE: volatile ---
    state = {"build_ts": int(time.time()), "service": "my-agent"}

    core_id = sha256(canon(core))
    profile_id = sha256(canon(profile))
    stable_id = sha256((core_id + profile_id).encode("utf-8"))

    return {
        "version":"1.0",
        "ids":{"core_id":core_id, "profile_id":profile_id, "stable_id":stable_id},
        "core":core, "profile":profile, "state":state
    }
