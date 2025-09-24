from fastapi import FastAPI
from pydantic import BaseModel, Field, confloat
from manifest import build_manifest
from agent import generate_reply

class DecodeOptions(BaseModel):
    temperature: confloat(ge=0.0, le=2.0) = Field(0.2, description="0=deterministico, >1 più creativo")
    top_p:      confloat(ge=0.0, le=1.0) = Field(0.9, description="nucleus sampling")

class InvokeReq(BaseModel):
    input: str
    options: DecodeOptions | None = None

with open("prompts/system.txt","r",encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

app = FastAPI()
MANIFEST = build_manifest()

@app.get("/manifest")
def get_manifest():
    return MANIFEST

@app.post("/invoke")
async def invoke(req: InvokeReq):
    opts = req.options or DecodeOptions()  # default
    out = await generate_reply(
        system_prompt=SYSTEM_PROMPT,
        user_input=req.input,
        temperature=opts.temperature,
        top_p=opts.top_p,
    )
    return {"output": out, "used_options": opts.model_dump()}
