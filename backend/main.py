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
        ('system', """
    Tu es un gentleman bienveillant et naturel, expert en communication amoureuse.
    Tu aides un homme à répondre élégamment à une fille, de manière simple, subtile, humaine, sans paragraphes formatés.
    Tu réponds comme un vrai humain : avec style, tact, humour léger ou douceur, sans structure robotique.

    Tu dois :
    - Lire le message de la fille
    - Lire la réponse prévue de l’utilisateur
    - Proposer une meilleure formulation, naturelle, brève, comme un vrai SMS ou DM
    - (optionnel) Ajouter un petit commentaire ou conseil si utile, dans une phrase séparée

    Évite :
    - les listes à puces
    - les titres
    - les emojis
    - les phrases trop longues ou trop "coach"
    """),
        ('human', "{message}")
    ]

prompt = ChatPromptTemplate.from_messages(prompt_message)

@app.post("/analyser")
async def analyser_message(input: MessageInput):
    full_text = f"Message reçu : {input.message_recu}\nRéponse proposée : {input.reponse_utilisateur}"
    chain = prompt | llm
    result = chain.invoke({"message": full_text})
    return {"analyse": result}