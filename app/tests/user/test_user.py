import pytest
from main import schema
from datetime import datetime

@pytest.mark.asyncio
async def test_add_user():
    add_user_mutation = """
            mutation testCreateUser {
                createUser(
                balance: 200, 
                email: "testuser@example.com", 
                name: "Test User", 
                password: "testpassword",
                interestId: 1)
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

    assert updated_user.errors is None
    assert updated_user.data['user']['email'] == "new_email@example.com"
    assert updated_user.data['user']['name'] == "My name"


# Tests updated interest for user 
@pytest.mark.asyncio 
async def test_user_interest_updated_for_user():

    # Sends mutation to update user interest 
    update_user_interest = """
            mutation updatesInterest($user_id: Int!, $interest_id: Int!) {
                updateInterestForUser(interestId: $interest_id, userId: $user_id)
            }
"""
    interest_update_variables = {
        "user_id": user_id, 
        "interest_id": 2
    }

    update_interest = await schema.execute(update_user_interest, variable_values=interest_update_variables)

    assert update_interest.errors is None

    # Confirms interest details have been updated once applied to user 
    check_user_interest_updated = """
            query updatesUser($user_id: Int!) {
                user(userId: $user_id) {
                    email
                    name
                    interests {
                        name
                        active
                        dateAdded
                        archived
                        dateArchived
                        id
                        }
                    
                }
            }
"""

    check_interest = await schema.execute(check_user_interest_updated, variable_values={"user_id": user_id})

    assert check_interest.errors is None
    interests = check_interest.data['user']['interests']

    # Check that the interest added is active
    assert interests[-1]['active'] == True
    assert interests[-1]['archived'] == False
    assert interests[-1]['dateArchived'] == None

    # Confirms user interest has been updated 
    check_interest_active_and_added = """
            query userInterest($user_id: Int!) {
                userInterest(userId: $user_id) {
                    id
                    active
                    created
                    userId
                    interestId
                }
            }
"""

    confirm_interest_active = await schema.execute(check_interest_active_and_added, variable_values={"user_id": user_id})
    print(confirm_interest_active)

    assert confirm_interest_active.errors is None
    assert confirm_interest_active.data['userInterest'][-1]['active'] == True
    assert confirm_interest_active.data['userInterest'][-1]['interestId'] == 2

    # Confirms all other user interests are INACTIVE 
    for interest in confirm_interest_active.data['userInterest'][:-1]:
        assert interest['active'] == False

    # Confirms the created date is today 
    last_interest = confirm_interest_active.data['userInterest'][-1]
    created_date = datetime.fromisoformat(last_interest['created']).date()
    today = datetime.now().date()
    assert created_date == today