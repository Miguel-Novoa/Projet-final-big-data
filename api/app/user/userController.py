# from fastapi import APIRouter, HTTPException
# from models import UserCreate, UserInDB
# from config import es
# import uuid
# from fastapi import HTTPException

# user_router = APIRouter()

# ES_INDEX = "users"

# def get_user_from_es(username: str):
#     """
#     Recherche un utilisateur par son nom d'utilisateur dans Elasticsearch.
#     """
#     try:
#         response = es.search(index="users", body={
#             "query": {
#                 "match": {
#                     "username": username
#                 }
#             }
#         })

#         # Vérifier si des résultats ont été trouvés
#         if response['hits']['total']['value'] > 0:
#             return response['hits']['hits'][0]['_source']
#         return None  # Aucun utilisateur trouvé
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error connecting to Elasticsearch")


# # Fonction de création d'un utilisateur dans Elasticsearch
# def create_user_in_es(user: UserCreate):
#     """
#     Crée un utilisateur dans Elasticsearch.
#     """
#     user_id = str(uuid.uuid4())  # Créer un ID unique pour l'utilisateur
#     user_data = user.dict()  # Convertir les données de l'utilisateur en dictionnaire
#     user_data["user_id"] = user_id  # Ajouter l'ID à l'utilisateur

#     try:
#         # Indexer l'utilisateur dans Elasticsearch
#         es.index(index="users", id=user_id, body=user_data)
#         return {**user_data, "user_id": user_id}  # Retourner les données de l'utilisateur créées
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error saving user to Elasticsearch")


# # Fonction de mise à jour d'un utilisateur dans Elasticsearch
# def update_user_in_es(username: str, user: UserCreate) -> dict:
#     doc = user.dict()
#     doc['password'] = user.password
#     es.update(index=ES_INDEX, id=username, doc={'doc': doc})
#     return doc

# # Fonction de suppression d'un utilisateur dans Elasticsearch
# def delete_user_from_es(username: str) -> bool:
#     try:
#         es.delete(index=ES_INDEX, id=username)
#         return True
#     except Exception:
#         return False




# @user_router.post("/users/", response_model=UserInDB)
# async def create_new_user(user: UserCreate):
#     # Vérifier si l'utilisateur existe déjà
#     if get_user_from_es(user.username):
#         raise HTTPException(
#             status_code=400,
#             detail="User already exists"
#         )
    
#     # Créer l'utilisateur dans Elasticsearch
#     created_user = create_user_in_es(user)
    
#     # Retourner l'utilisateur avec les informations nécessaires
#     return UserInDB(**created_user)

# @user_router.get("/users/{username}", response_model=UserInDB)
# async def get_user(username: str):
#     user = get_user_from_es(username)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
#     return UserInDB(**user)

# @user_router.put("/users/{username}", response_model=UserInDB)
# async def update_user(username: str, user: UserCreate):
#     existing_user = get_user_from_es(username)
#     if not existing_user:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
#     updated_user = update_user_in_es(username, user)
#     return UserInDB(**updated_user)

# @user_router.delete("/users/{username}")
# async def delete_user(username: str):
#     if not delete_user_from_es(username):
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
#     return {"msg": f"User {username} has been deleted"}
