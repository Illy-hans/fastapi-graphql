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

