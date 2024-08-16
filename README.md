## Interest Calculator - Backend

A finance app that calculates how much money has been accrued in an interest savings account daily. The tech stack used includes: Python, FastAPI, GraphQL, Strawberry, SQLAlchemy/Postgres. Celery for automating daily balance updates with Redis as broker and Pytest for testing. 

### To run

Python, Pip, Postgres and Docker need to be installed locally. 

Create a .env file with the following variables: 

```bash 
DB_NAME= DB name for project
USER= Your Postgres username 
PASSWORD= Your Posgres password
HOST='localhost'
PORT= '5432' 

# These are for authentication purposes
secret='chooseArandomstring'
algorithm='HS256'
```

Create the virtual environment and install dependencies:

```bash
$ pipenv shell 
$ pipenv install 
```

Ensure Docker desktop is running, build the image and run the container

```bash
$ docker build --tag YOUR_DIRECTORY_NAME . 
$ docker run --publish 8000:8000 YOUR_DIRECTORY_NAME
```

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
    - [x] Password hashing
    - [ ] Tokens introduction/ Log-in & Logout
    - [ ] Add admin user

</details>