#!/usr/bin/env python3
"""Module of Basic_auth."""

import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith("Basic "):
            return "".join(authorization_header.split(" ")[1:])
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode a Base64 authorization header."""
        if (base64_authorization_header
                and isinstance(base64_authorization_header, str)):
            try:
                decoded = base64.b64decode(
                    base64_authorization_header
                )
                return decoded.decode("utf-8")
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract the user email and password."""
        if (decoded_base64_authorization_header
                and isinstance(decoded_base64_authorization_header, str)
                and ":" in decoded_base64_authorization_header):
            email, password = decoded_base64_authorization_header.split(
                ":", 1
            )
            return email, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Get the User object from credentials."""
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        for user in users:
            if user and user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current authenticated user."""
        if request is None:
            return None

        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        extracted = self.extract_base64_authorization_header(auth_header)

        if extracted is None:
            return None

        decoded = self.decode_base64_authorization_header(extracted)

        if decoded is None:
            return None

        email, password = self.extract_user_credentials(decoded)

        return self.user_object_from_credentials(email, password)
