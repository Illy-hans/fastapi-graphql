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


@pytest.mark.asyncio
async def test_add_user():
    add_user_mutation = """
            mutation testCreateUser {
                createUser(
                balance: 200, 
                email: "testuser@example.com", 
                name: "Test User", 
                password: "testpassword")
            }
"""

    result = await schema.execute(add_user_mutation)
    print(result)

    assert result.errors == None
    assert result.data["createUser"] == 'User added successfully'


@pytest.mark.asyncio
async def test_email_in_use():
    add_user_mutation = """
            mutation testCreateUser {
                createUser(
                balance: 200, 
                email: "testuser@example.com", 
                name: "Test User", 
                password: "testpassword")
            }
"""

    result = await schema.execute(add_user_mutation)

    assert result.errors == None
    assert result.data["createUser"] == 'Email address is in use'


# token variable to be re-used in decode token
auth_token = None 

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
user_id = None

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



