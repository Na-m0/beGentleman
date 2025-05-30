pip install langchain                                                       
pip install langchain-core                                                                                                                                                
pip install langchain-mistralai
pip install fastapi uvicorn pydantic

Pour tout insataller DIRECTEMENT : pip install -r requirements.txt

pour mettre l'environnement : python -m venv venv 
pour aller en environnement virtuel et pouvoir lancer (sur windows) : venv\Scripts\activate
pour lancer l'api : uvicorn main:app --reload