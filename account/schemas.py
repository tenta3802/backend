from rest_framework import serializers
from drf_spectacular.utils import inline_serializer, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes

# Token API
USER_SIGNIN_REQUEST = {
    "application/json": inline_serializer(
        name="user sign",
        fields={
            "user_id": serializers.CharField(),
            "password": serializers.CharField(),
        },
    ),
}

USER_SIGNIN_RESPONSES = {
    200: inline_serializer(
        name="success",
        fields={
            "access": serializers.CharField(),
            "refresh": serializers.CharField()
            }
        ),
    400: OpenApiTypes.OBJECT,
}
USER_SIGNIN_EXAMPLES = [
    OpenApiExample(
        response_only=True,
        name="Login Failed",
        summary="Login Failed",
        value={
           "message": "user_id and password are required"
        },
        status_codes=["400"],
    ),
    OpenApiExample(
        response_only=True,
        name="User Error",
        summary="Login Failed",
        value={"message": "Does Not Exist User"},
        status_codes=["400"],
    ),
    OpenApiExample(
        response_only=True,
        name="Invalid Password",
        summary="Login Failed",
        value={"message": "Invalid Password"},
        status_codes=["400"],
    ),
]