#!/usr/bin/env python3
"""Basic Auth module.
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Authentication class.
    """

    def extract_base64_authorization_header(self, authorization_header):
        """Returns the Base64 part of the Authorization header."""
        if type(authorization_header) is not str:
            return None

        prefix = "Basic "
        if not authorization_header.startswith(prefix):
            return None

        return authorization_header[len(prefix):]

    def decode_base64_authorization_header(self, base64_authorization_header):
        """Returns the decoded value of a Base64 string."""
        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header):
        """Returns user email and password from decoded Base64 string."""
        if type(decoded_base64_authorization_header) is not str:
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(
            ":", 1
        )
        return email, password

    def user_object_from_credentials(self, user_email, user_pwd):
        """Returns the User instance based on email and password."""
        if type(user_email) is not str or type(user_pwd) is not str:
            return None

        users = self.user_with_email(user_email)

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None):
        """Returns the current authenticated user."""
        authorization_header = self.authorization_header(request)

        if authorization_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(
            authorization_header
        )

        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(
            base64_header
        )

        if decoded_header is None:
            return None

        email, password = self.extract_user_credentials(decoded_header)

        return self.user_object_from_credentials(email, password)
