from fastapi import FastAPI
from pydantic import BaseModel
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    api_key="LS05kJiWyNo61YiAAz0uKIof25UqUec4"
)

prompt_message = [
    ('system', "tu es un assistant chargé d'analyser le message d'un utilisateur et de fournir une réponse optimisée."),
    ('human', "{message}")
]
prompt = ChatPromptTemplate.from_messages(prompt_message)

class MessageInput(BaseModel):
    message_recu: str
    reponse_utilisateur: str

@app.post("/analyser")
async def analyser_message(input: MessageInput):
    full_text = f"Message reçu : {input.message_recu}\nRéponse proposée : {input.reponse_utilisateur}"
    chain = prompt | llm
    result = chain.invoke({"message": full_text})
    return {"analyse": result}