import pytest
from app.db.session import get_session
from app.resolvers.user.user_query_resolvers import get_all_users
from main import schema

@pytest.mark.asyncio
async def test_all_users_graphql():
    get_all_users_query = """
            query TestAllUsers {
                    users {
                        id
                        email
                        name
                        balances {
                            id
                        }
                        interests {
                            id
                        }
                    }
                }
        """

    result1 = await schema.execute(get_all_users_query)
    users1 = result1.data["users"]
    result2 = await schema.execute(get_all_users_query)
    users2 = result1.data["users"]


    assert result1.errors == None
    assert result2.errors == None

    assert len(users1) == len(users2)
    
#     #Iterate over list of users and ensure every user has an id
    for user in users1:
        assert user.get('id') is not None

    for user in users2:
        assert user.get('id') is not None



@pytest.mark.asyncio
async def test_all_users_():
    async with get_session() as db_session:

        result1 = await get_all_users(db_session)
        result2 = await get_all_users(db_session)

        users1 = result1
        users2 = result2
        assert len(users1) == len(users2)

        for user in users1:
            assert user.id is not None
