import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schemas.mutation_schema import Mutation
from app.schemas.query_schema import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)

def create_app():
    
    app = FastAPI()
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

    return app


app= create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)