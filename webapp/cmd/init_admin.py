"""
Initialize admin user in the database.
Username: admin
Password: admin
"""
from webapp.web import create_app
from webapp.models.user_model import User


def main():
    """Create or update the admin user."""
    app = create_app()

    with app.app_context():
        # Check if admin user already exists
        admin_user = User.objects(username="admin").first()

        if admin_user:
            print("Admin user already exists. Updating password...")
            admin_user.set_password("admin")
            admin_user.role = "admin"
            admin_user.save()
            print("✓ Admin password updated")
        else:
            print("Creating new admin user...")
            admin_user = User(username="admin")
            admin_user.set_password("admin")
            admin_user.role = "admin"
            admin_user.save()
            print("✓ Admin user created successfully")

        print(f"Username: admin")
        print(f"Password: admin")


if __name__ == "__main__":
    main()
