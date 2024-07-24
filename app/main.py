import strawberry
from typing import List
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Author:
        name: str
        book: str
        
authors = [
    Author(name="me", book="too"),
    Author(name="George Orwell", book="1984"),
]

@strawberry.type
class Query:
    @strawberry.field
    def all_authors(self) -> List[Author]:
        return authors

@strawberry.type
class Mutation:
    @strawberry.field
    def add_author(self, name: str) -> str:
        authors.append(name)
        return name

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")