## Interest Calculator - Backend

A finance app that calculates how much money has been accrued in an interest savings account daily. The tech stack used includes: Python, FastAPI, Graphql, Strawberry, SQLAlchemy/Postgres. Celery will be used for automating daily balance updates(message broker tbc) and Pytest for testing.

So far users can: 
- Create an account with an initial balance amount
- An interest type can be applied to a users account 
- Users can have multiple interest types, with only one active at a time


### Roadmap
- [x] Build structure
- [x] User & Interest models
- [x] Database connection
    - [x] Set up 
    - [x] Sessions
- [ ] GraphQL
    - [ ] User 
        - [x] queries
        - [ ] mutations
    - [ ] Interest 
        - [x] queries 
        - [ ] mutations
- [ ] Resolvers
    - [ ] User 
        - [x] GET all_users, user
        - [x] POST add_user
        - [x] PATCH add_interest, update_user_data
        - [x] DELETE delete_user
    - [ ] Interest 
        - [x] GET all_interests, interest
        - [x] POST add_new_interest
        - [x] PATCH archive_interest - updates archived attribute 
- [ ] Add Balance model for historial accuracy
    - [x] Balance model
    - [ ] GET percentage of interest 
    - [x] Update User query to load balances
    - [x] Add first balance to user creation
    - [ ] UPDATE(Add) user balance
- [ ] Celery - balance automation
    - [ ] Choose message broker - Postgres/ Redis?
    - [ ] create service to queue automated balance calculations daily
- [ ] Authentication
    - [ ] Password hashing
    - [ ] Tokens introduction
    - [ ] Add admin user