from server.models.user import UserGenerations as UserGenerationsDB
from server.database import SessionLocal

db = SessionLocal()

def create_user_generation(username, input_data, generation, application, tag):
    user_gen = UserGenerationsDB(
        username = username,
        input_data = input_data,
        generation = generation,
        application = application,
        tag = tag
    )

    # Add and Commit database
    db.add(user_gen)
    db.commit()

    return ( user_gen, 'User Generated Data Added' )