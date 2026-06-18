from functools import wraps

from flask import g, jsonify, request

from app.services.auth_service import (
    ServiceError,
    authenticate_token,
)


def jwt_required(view_function):
    @wraps(view_function)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get(
            "Authorization",
            "",
        )

        parts = authorization.split()

        if (
            len(parts) != 2
            or parts[0].lower() != "bearer"
        ):
            return jsonify(
                error="Bearer token is required"
            ), 401

        token = parts[1]

        try:
            user, session = authenticate_token(token)
        except ServiceError as error:
            return jsonify(
                error=error.message
            ), error.status_code

        g.current_user = user
        g.current_session = session
        g.current_token = token

        return view_function(*args, **kwargs)

    return wrapped
