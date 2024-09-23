from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from src.dependencies.get_graphql_context import get_graphql_context
from src.graphql_schemas.trade_mark_schema import Query


schema = Schema(Query)

trade_mark_router = GraphQLRouter(
    schema=schema,
    path='/trade_mark/graphql',
    context_getter=get_graphql_context
)
