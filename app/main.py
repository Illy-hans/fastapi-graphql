import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


schema = strawberry.Schema(query=Query, mutation=Mutation)

def create_app():
    
    app = FastAPI()
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

    return app