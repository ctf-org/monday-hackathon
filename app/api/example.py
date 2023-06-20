from fastapi import APIRouter
from langchain.llms import OpenAI

router = APIRouter()

@router.get("/")
async def example():
    return {"it": "works"}

@router.get("/example")
async def example():
    llm = OpenAI(temperature=0.9)
    text = "What would be a good company name for a company that makes colorful socks?"
    return {text: llm(text).strip()}
