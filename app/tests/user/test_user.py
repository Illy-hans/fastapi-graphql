import pytest
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_session
from app.models.balance_model import Balance as BalanceModel
from app.models.interest_model import Interest as InterestModel
from app.models.user_model import User as UserModel
from app.resolvers.user.user_mutation_resolvers import add_user
from app.utils.authentication import Authentication
from app.utils.password_hasher import Hasher
from main import schema


# @pytest.mark.asyncio
# async def test_add_user():
#     add_user_mutation = """
#             mutation testCreateUser {
#                 createUser(
#                 balance: 200, 
#                 email: "testuser@example.com", 
#                 name: "Test User", 
#                 password: "testpassword")
#             }
# """

#     result = await schema.execute(add_user_mutation)
#     print(result)

#     assert result.errors == None
#     assert result.data["createUser"] == 'User added successfully'


# @pytest.mark.asyncio
# async def test_email_in_use():
#     add_user_mutation = """
#             mutation testCreateUser {
#                 createUser(
#                 balance: 200, 
#                 email: "testuser@example.com", 
#                 name: "Test User", 
#                 password: "testpassword")
#             }
# """

#     result = await schema.execute(add_user_mutation)

#     assert result.errors == None
#     assert result.data["createUser"] == 'Email address is in use'


# token variable to be re-used in decode token
auth_token: str = None 

@pytest.mark.asyncio
async def test_create_token_for_user():
    create_token_mutation = """
            mutation MyMutation {
                login(email: "testuser@example.com", password: "testpassword") {
                accessToken
                userName
                }
            }
"""

    result = await schema.execute(create_token_mutation)
    print(result)

    assert result.errors == None
    token = result.data['login']["accessToken"]
    assert token != ""

    global auth_token
    auth_token = token
    print(auth_token)


# user_id variable to be used in subsequent tests
user_id: int = None

@pytest.mark.asyncio 
async def test_decode_token():
    decode_token_mutation_return_user = """
            mutation DecodeToken($token: String!) {
                decodeUserFromToken(token: $token) {
                    name
                    email
                    id
                }
            }
"""

    result = await schema.execute(decode_token_mutation_return_user, variable_values={"token": auth_token})
    
    assert result.errors is None
    assert result.data['decodeUserFromToken']['name'] == "Test User"
    assert result.data['decodeUserFromToken']['email'] == "testuser@example.com"
    assert result.data['decodeUserFromToken']['id'] != None

    global user_id 
    user_id = result.data['decodeUserFromToken']['id']


@pytest.mark.asyncio
async def test_update_user():
    update_user_info_mutation = """
            mutation testUpdateUser($user_id: Int!, $user: UserInput!) {
            updateUser(user: $user, userId: $user_id)
        }
    """

    user_data = {
        "email": "new_email@example.com",
        "name": "My name"
    }

    result = await schema.execute(update_user_info_mutation, variable_values={"user_id": user_id, "user": user_data})

    assert result.errors is None
    assert result.data['updateUser'] == "User details updated successfully"

    check_user_updated = """
            query updatesUser($user_id: Int!) {
                user(userId: $user_id) {
                    email
                    name
                }
            }
"""

    updated_user = await schema.execute(check_user_updated, variable_values={"user_id": user_id})
    print(updated_user)

    assert updated_user.errors is None
    assert updated_user.data['user']['email'] == "new_email@example.com"
    assert updated_user.data['user']['name'] == "My name"


