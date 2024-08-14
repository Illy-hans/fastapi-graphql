import pytest
from main import schema

# Sets global percentage to be used 
percentage_for_user: int = None

@pytest.mark.asyncio
async def test_get_percentage():

# Create new user
    add_user_mutation = """
            mutation testCreateUser {
                createUser(
                balance: 300, 
                email: "percentageUser@example.com", 
                name: "Percentage user", 
                password: "testpassword",
                interestId: 1)
            }
"""

    add_user_result = await schema.execute(add_user_mutation)

    assert add_user_result.errors == None
    assert add_user_result.data["createUser"] == 'User added successfully'

# Login 
    create_token_mutation = """
            mutation MyMutation {
                login(email: "percentageUser@example.com", password: "testpassword") {
                accessToken
                userName
                }
            }
"""

    token_result = await schema.execute(create_token_mutation)

    assert token_result.errors == None
    token = token_result.data['login']["accessToken"]
    assert token != ""


# Decode token to get user_id
    decode_token_mutation_return_user = """
                mutation DecodeToken($token: String!) {
                    decodeUserFromToken(token: $token) {
                        name
                        email
                        id
                    }
                }
    """

    decoded_token_result = await schema.execute(decode_token_mutation_return_user, variable_values={"token": token})
        
    assert decoded_token_result.errors is None
    assert decoded_token_result.data['decodeUserFromToken']['name'] == "Percentage user"
    assert decoded_token_result.data['decodeUserFromToken']['email'] == "percentageUser@example.com"
    assert decoded_token_result.data['decodeUserFromToken']['id'] != None

    user_id = decoded_token_result.data['decodeUserFromToken']['id']


# Get interest_percentage
    get_interest_percentage = """
            query getPercentage($user_id: Int!){
                getInterestPercentage(userId: $user_id)
            }
"""

    interest_percentage = await schema.execute(get_interest_percentage, variable_values={"user_id": user_id})

    assert interest_percentage.errors is None
    assert interest_percentage.data['getInterestPercentage'] == 7