from app.extensions import db
from app.models import User


def find_by_email(email):
    statement = db.select(User).filter_by(email=email)

    return db.session.execute(
        statement
    ).scalar_one_or_none()


def create_user(name, email, password_hash):
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    db.session.add(user)
    db.session.commit()

    return user