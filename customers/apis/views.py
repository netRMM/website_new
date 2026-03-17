from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
import requests
import os

class EmailValidationView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"validation_result_{email}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return Response(cached_result)

        base_url = 'https://api.validemail.net/'
        token = 'fc1778482d204ad7a11b20818816f905'

        params = {
            'email': email,
            'token': token
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # if not data.get('IsValid', False) or data.get('State') != 'Deliverable':
            #     return Response({"message": "Email is not valid or deliverable."})

            if data.get('Disposable', False):
                return Response({"message": "Temporary emails are not allowed."})

            # Infer business email: Not free, not disposable, not role-based
            if data.get('Free', False) or data.get('Role', False):
                return Response({"message": "Only business emails are allowed."})

            # Here you can add more validations if needed

            # If all checks pass
            result = {"message": "Email is available for registration."}
            cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour

            return Response(result)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
