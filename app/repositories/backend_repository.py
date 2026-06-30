from app.extensions import db
from app.models import BackendRegistration


def create_backend(
    user_id,
    service_name,
    target_url,
    api_key,
):
    backend = BackendRegistration(
        user_id=user_id,
        service_name=service_name,
        target_url=target_url,
        api_key=api_key,
    )

    db.session.add(backend)
    db.session.commit()

    return backend


def list_backends_by_user(user_id):
    statement = (
        db.select(BackendRegistration)
        .filter_by(user_id=user_id)
        .order_by(
            BackendRegistration.created_at.desc()
        )
    )

    return db.session.execute(
        statement
    ).scalars().all()
def find_owned_backend(backend_id, user_id):
    statement = db.select(
        BackendRegistration
    ).filter_by(
        id=backend_id,
        user_id=user_id,
    )

    return db.session.execute(
        statement
    ).scalar_one_or_none()


def save_backend(backend):
    db.session.commit()

    return backend
def find_active_by_api_key(api_key):
    return (
        BackendRegistration.query
        .filter_by(
            api_key=api_key,
            is_active=True
        )
        .first()
    )