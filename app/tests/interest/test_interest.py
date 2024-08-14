from datetime import datetime
from main import schema
import pytest

# Get all interest types
@pytest.mark.asyncio
async def test_get_all_interests():
    get_all_interests = """
            query allInterests {
                interests {
                    id
                    name
                    percentage
                    dateAdded
                    dateArchived
                    archived
                    active
                }
            }
"""

    all_interests1 = await schema.execute(get_all_interests)
    interests1 = all_interests1.data["interests"]
    all_interests2 = await schema.execute(get_all_interests)
    interests2 = all_interests2.data["interests"]

    assert len(interests1) == len(interests2)

    interests = all_interests1.data['interests']

    for id in interests:
        assert id is not None

# Test add new interest type
@pytest.mark.asyncio
async def test_add_interest_type():
    add_interest = """
            mutation addInterest {
                addNewInterest(interest: 
                {
                name: "New deal 2024", 
                percentage: 9.5
                })
            }
"""

    add_interest_result = await schema.execute(add_interest)

    assert add_interest_result.errors == None
    assert add_interest_result.data['addNewInterest'] == 'Interest added successfully'
    

# Test uniqueness of interest type's name 
@pytest.mark.asyncio
async def test_interest_name_in_use():
    add_interest = """
            mutation addInterest {
                addNewInterest(interest: 
                {
                name: "New deal 2024", 
                percentage: 9.5
                })
            }
"""

    add_interest_result = await schema.execute(add_interest)

    assert add_interest_result.errors == None
    assert add_interest_result.data['addNewInterest'] == 'Interest name already in use'


# GET interest by ID
@pytest.mark.asyncio
async def test_get_interest_by_id():
    get_interest = """
            query getInterest($interest_id: Int!) {
                getInterest(interestId: $interest_id) {
                    id
                    name
                    percentage
            }
        }
"""
    interest_id_to_get = {
        "interest_id": 5
    }

    get_interest_result = await schema.execute(get_interest, variable_values=interest_id_to_get)

    assert get_interest_result.errors is None
    assert get_interest_result.data['getInterest']['id'] == 5
    assert get_interest_result.data['getInterest']['name'] == 'New deal 2024'
    assert get_interest_result.data['getInterest']['percentage'] == 9.5


@pytest.mark.asyncio
async def test_archive_interest():
    archive_interest = """
            mutation archiveInterest($interest_id: Int!) {
                archiveInterest(interestId: $interest_id)
            }
"""

    interest_to_archive = {
        "interest_id": 5
    }


    archived_interest = await schema.execute(archive_interest, variable_values=interest_to_archive)

    assert archived_interest.errors is None
    assert archived_interest.data['archiveInterest'] == 'Interest archived successfully'


    get_archived_interest = """
            query getInterest($interest_id: Int!) {
                getInterest(interestId: $interest_id)  {
                    archived
                    id
                    percentage
                    name
                    dateArchived
                }
            }
"""

    interest_id_to_get = {
        "interest_id": 5
    }

    get_archived_interest_result = await schema.execute(get_archived_interest, variable_values=interest_id_to_get)

    assert get_archived_interest_result.errors is None
    assert get_archived_interest_result.data['getInterest']['id'] == 5
    assert get_archived_interest_result.data['getInterest']['archived'] == True
    assert get_archived_interest_result.data['getInterest']['name'] == 'New deal 2024'

    interest = get_archived_interest_result.data['getInterest']
    archived_date = datetime.fromisoformat(interest['dateArchived']).date()
    today = datetime.now().date()
    assert archived_date == today

