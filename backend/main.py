from fastapi import FastAPI
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from model import MessageInput

app = FastAPI()

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    api_key="LS05kJiWyNo61YiAAz0uKIof25UqUec4"
)

prompt_message = [
    ('system', "tu es un coach en séduction hyper gentleman, et tu es chargé d'analyser le message recu par une jeune demoiselle et de fournir une réponse optimisée pour aider un jeune disciple gentleman pour qu'il puisse obtenir plus avec cette fille."),
    ('human', "{message}")
]
prompt = ChatPromptTemplate.from_messages(prompt_message)

@app.post("/analyser")
async def analyser_message(input: MessageInput):
    full_text = f"Message reçu : {input.message_recu}\nRéponse proposée : {input.reponse_utilisateur}"
    chain = prompt | llm
    result = chain.invoke({"message": full_text})
    return {"analyse": result}