#  Copyright (c) 2023 - Muzaffar Makhkamov
#
#
#  This file is part of  "Django JsonRPC Server Template".
#
#  "Django JsonRPC Server Template" is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  "Django JsonRPC Server Template" is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with "Django JsonRPC Server Template".  If not, see <http://www.gnu.org/licenses/>.
from functools import wraps

from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Result, Success, dispatch, Error
from jsonschema import ValidationError
from rest_framework import serializers

from v1.modules import authorization
from v1.services.sample import methods
from v1.utils.decorators import requires_json
from v1.utils.helper import json_response


@method(name="login")
def login(context, username, password, refresh=False) -> Result:
    response = authorization.login(username=username, password=password, refresh=refresh)
    return response_handler(response)


@method
def ping(context) -> Result:
    return Success("pong")


def validate_params(serializer_class):
    def decorator(func):
        @wraps(func)
        def wrapper(context, **params):
            serializer = serializer_class(data=params)
            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            return func(context, **serializer.validated_data)

        return wrapper

    return decorator


class TransferCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField(min_length=16, max_length=19)
    expire = serializers.CharField(min_length=4, max_length=5)  # MMYY or MM/YY
    amount = serializers.IntegerField(min_value=1000)





@method
@validate_params(TransferCreateSerializer)
def transfer_create(context, card_number: str, expire: str, amount: int) -> Result:
    return Success("pong")


@method
def get_users(context) -> Result:
    return Success("pong")


@method(name="cbu.rates")
def btc_price(context) -> Result:
    response = methods.get_rates()
    return Success(response)


@csrf_exempt
@requires_json
def jsonrpc(request):
    context = {
        'user': request.user
    }

    response = dispatch(request.data, context=context)

    return json_response(response)


def response_handler(response):
    if 'result' in response:
        return Success(response['result'])
    if 'error' in response:
        return Error(response['error']['code'], response['error']['message'])
    else:

        return Error(response)
