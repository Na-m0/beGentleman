from pydantic import BaseModel

class MessageInput(BaseModel):
    message_recu: str
    reponse_utilisateur: str