from server.models.user import User as UserDB

from server.db.session import SessionLocal

from server.utils.auth_handler import verify_password, get_password_hash

db = SessionLocal()

def check_user(user):
    '''
    Check if a user exists with the same username
    '''

    user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not user:
        return ( None, 'User does not exists' )
    return ( user, 'User exists' )

def get_users():
    '''
    Get all users
    '''

    users = db.query(UserDB).all()
    if users:
        return ( users, 'Fetched Users' )
    else:
        return (False, 'No Users Present')

def get_user(username: str):
    '''
    Get user with username
    '''

    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        return ( None, 'No such User' )
    return ( user, 'Fetched the User' )

def create_user(user):
    '''
    Add user to the database with unique username
    '''
    
    ret, msg = check_user(user)
    if ret:
        return ( False, msg )
    else:
        user = UserDB(
            username= user.username,
            email = user.email,
            password = get_password_hash(user.password)
        )

        # Add and Commit database
        db.add(user)
        db.commit()
        
        return ( user, 'User Registered' )

# Update a user with a matching ID
def update_user(username: str, user_data: dict):

    ret, msg = get_user(username)
    if not ret:
        return ( ret, msg )
    ret.username = user_data.username
    ret.email = user_data.email
    ret.password = get_password_hash(user_data.password)
    
    db.commit()

    return ( ret, 'Updated user' )

# Delete a user from the database
def delete_user(username: str):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user:
        db.delete(user)
        db.commit()

        return ( True, 'User Deleted' )
    return ( False, 'User not Deleted' )

def authenticate_user(username: str, password: str):
    
    ret, msg = get_user(username)
    if not ret:
        return ( False, msg )
    
    if not verify_password( password, ret.password ):
        return ( False, 'Password verification failed' )
    return ( ret, 'User Authenticated' )

