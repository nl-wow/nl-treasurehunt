from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()  # This will make the current app context

def make_user_admin(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_admin = True
        db.session.commit()
        return f"User {user.username} has been set as an admin."
    return "User not found."

if __name__ == '__main__':
    import sys
    try:
        username = sys.argv[1]  # Take username from the command line argument
    except IndexError:
        print("Please provide a username.")
        sys.exit(1)

    print(make_user_admin(username))
