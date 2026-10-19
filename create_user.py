from app import app, db, User  # Ensure app.py is in the same directory

def create_user(username, password):
    with app.app_context():
        if User.query.filter_by(username=username).first():
            print("User already exists.")
            return

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' created successfully.")

if __name__ == "__main__":
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    create_user(username, password)
