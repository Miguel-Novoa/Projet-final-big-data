from fastapi import FastAPI
# from user.userController import user_router
# from config import es

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is connected to Elasticsearch!"}

# @app.get("/search/")
# async def search(index: str, query: str):
#     """
#     Endpoint pour rechercher des données dans Elasticsearch.
#     """
#     try:
#         response = es.search(index=index, body={"query": {"match": {"_all": query}}})
#         return response['hits']['hits']
#     except Exception as e:
#         return {"error": str(e)}

# Inclure le routeur utilisateur
# app.include_router(user_router)
