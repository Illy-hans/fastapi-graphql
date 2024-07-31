## Interest Calculator - Backend

A finance app that calculates how much money has been accrued in an interest savings account daily.

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
        - [ ] PATCH archive_interest - updates archived attribute 
- [ ]  Add new model for Balance 
    - [ ] Celery to queue automated balance calculations
- [ ] Authentication
    - [ ] Password hashing
    - [ ] Tokens introduction
    - [ ] Add admin user