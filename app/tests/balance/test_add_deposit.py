from datetime import datetime
import pytest
from main import schema

@pytest.mark.asyncio
async def test_update_balance():

# Create new user
    add_user_mutation = """
            mutation testCreateUser {
                createUser(
                balance: 300, 
                email: "balanceUser@example.com", 
                name: "Balance user", 
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
                login(email: "balanceUser@example.com", password: "testpassword") {
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
    assert decoded_token_result.data['decodeUserFromToken']['name'] == "Balance user"
    assert decoded_token_result.data['decodeUserFromToken']['email'] == "balanceUser@example.com"
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


# Test updated balance
    add_deposit = """
            mutation addDeposit($user_id: Int!, $deposit: Float!)  {
                addDeposit(deposit: $deposit, userId: $user_id)
            }
"""

    deposit_details = {
        "user_id": user_id,
        "deposit": 550.50,
    }

    added_deposit = await schema.execute(add_deposit, variable_values=deposit_details)

    assert added_deposit.errors is None

    new_user_balance = """
        query user($user_id: Int!) {
            user(userId: $user_id) {
                balances {
                date
                cumulativeInterestAccrued
                interestAccruedToday
                id
                totalBalance
                userId
                }
                id
            }
        }
"""

    user_balance_updated = await schema.execute(new_user_balance, variable_values={"user_id": user_id})

    assert user_balance_updated.errors is None 
    assert user_balance_updated.data['user']['id'] == user_id

    last_balance = user_balance_updated.data['user']['balances'][-1]
    assert last_balance['totalBalance'] == 850.50
    assert last_balance['cumulativeInterestAccrued'] == 0 
    assert last_balance['interestAccruedToday'] == 0

    created_date = datetime.fromisoformat(last_balance['date']).date()
    today = datetime.now().date()
    assert created_date == today




