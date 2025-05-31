from fastapi import FastAPI
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from model import MessageInput

app = FastAPI()

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.2,
    api_key="LS05kJiWyNo61YiAAz0uKIof25UqUec4"
)

prompt_message = [
    ('system', """Tu es un coach en séduction à la fois gentleman et naturel. 
Tu n'es pas un robot, mais un gentleman qui donne des conseils utiles et naturels. 
Analyse le message reçu et la réponse prévue, puis propose une réponse plus naturelle et gentleman, comme si tu écrivais un vrai message à envoyer à la fille. 
Analyse le message de la dame et propose une analyse complete de ce que le message peut dire et essaye de faire la réponse la plus gentleman possible donc pas de message trop niai avec des émoji, ici on est des hommes qui veut séduire rien d'autre """),
    ('human', "{message}")
]

prompt = ChatPromptTemplate.from_messages(prompt_message)

@app.post("/analyser")
async def analyser_message(input: MessageInput):
    full_text = f"Message reçu : {input.message_recu}\nRéponse proposée : {input.reponse_utilisateur}"
    chain = prompt | llm
    result = chain.invoke({"message": full_text})
    return {"analyse": result}