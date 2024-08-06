## Interest Calculator - Backend

A finance app that calculates how much money has been accrued in an interest savings account daily. The tech stack used includes: Python, FastAPI, Graphql, Strawberry, SQLAlchemy/Postgres. Celery will be used for automating daily balance updates with Redis as broker and Pytest for testing.

So far users can: 
- Users can create an account with an initial balance amount
- Users can have multiple interest types, with only one active at a time
- A users account can be deleted
- An interest type can be applied to a users account 

<details>
<summary> Roadmap </summary>
</br>

- [x] Build structure
- [x] User & Interest models
- [x] Database connection
    - [x] Set up 
    - [x] Sessions
- [x] GraphQL
    - [ ] User 
        - [x] queries
        - [x] mutations
    - [x] Interest 
        - [x] queries 
        - [x] mutations
- [x] Resolvers
    - [x] User 
        - [x] GET all_users, user
        - [x] POST add_user
        - [x] PATCH add_interest, update_user_data
        - [x] DELETE delete_user
    - [x] Interest 
        - [x] GET all_interests, interest
        - [x] POST add_new_interest
        - [x] PATCH archive_interest - updates archived attribute 
- [x] Add Balance model for historial accuracy
    - [x] Balance model
    - [x] GET percentage of interest 
    - [x] Update User query to load balances
    - [x] Add first balance to user creation
    - [x] UPDATE(Add) user balance
    - [x] Add daily balance update function
- [ ] Celery - balance automation
    - [x] install and set up Redis
    - [x] create service to queue automated balance calculations daily
- [ ] Authentication
    - [ ] Password hashing
    - [ ] Tokens introduction/ Log-in & Logout
    - [ ] Add admin user

</details>