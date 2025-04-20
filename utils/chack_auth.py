from datetime import datetime, timedelta
from random import randint
from functools import wraps
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from lock.models import ParentConnectChild, Application
from tariff.models import SaleTariff
from rest_framework.exceptions import APIException


def generate_sms_code():
    return randint(100000, 999999)


class IPThrottle(UserRateThrottle):
    rate = '5/min'


def allowed_only_admin():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator


def permission(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator


def check_connection(parent, child):
    if not ParentConnectChild.objects.filter(parent=parent, child=child, is_active=True).exists():
        raise ValidationError({'detail': 'No active connection with the child.'}, 400)


FREE_USE_DAY = 1


class CustomAPIException(APIException):
    status_code = 400

    def __init__(self, detail, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=detail)


# 700 - sotib olinmagan tariff
# 701 - sotib olingan lekin vaqti tugagan tariff


def check_tariff_child(child, tariff):
    connection = ParentConnectChild.objects.filter(child=child).first()
    if connection:
        first_connection = ParentConnectChild.objects.filter(parent=connection.parent, first_connection=True).first()
        if first_connection:
            if first_connection.date and first_connection.date >= datetime.now() - timedelta(days=FREE_USE_DAY):
                return True
            else:
                sale_tariff = SaleTariff.objects.filter(child=child, tariff__name=tariff).first()
                if sale_tariff:
                    if sale_tariff.start_date <= datetime.now() <= sale_tariff.end_date:
                        return True
                    else:
                        sale_tariff.status = False
                        sale_tariff.save()
                        if tariff == 'lock':
                            Application.objects.filter(child=child, locked=True).update(
                                locked=False, start_lock=None, end_lock=None)
                        raise CustomAPIException({'detail': 701})
                else:
                    raise CustomAPIException({'detail': 700})
        else:
            raise CustomAPIException({'detail': 'First connection not found.'}, 404)
    else:
        raise CustomAPIException({'detail': 'There is no connection with any parents.'})


def check_tariff_parent(parent, child, tariff):
    connection = ParentConnectChild.objects.filter(parent=parent, child=child).first()
    if not connection:
        raise CustomAPIException({'detail': 'There is no connection with the child.'})
    first_connection = ParentConnectChild.objects.filter(parent=connection.parent, first_connection=True).first()
    if first_connection:
        if first_connection.date and first_connection.date >= datetime.now() - timedelta(days=FREE_USE_DAY):
            return True
        else:
            sale_tariff = SaleTariff.objects.filter(child=child, tariff__name=tariff).first()
            if sale_tariff:
                if sale_tariff.start_date <= datetime.now() <= sale_tariff.end_date:
                    return True
                else:
                    sale_tariff.status = False
                    sale_tariff.save()
                    if tariff == 'lock':
                        Application.objects.filter(child=child, locked=True).update(
                            locked=False, start_lock=None, end_lock=None)
                    raise CustomAPIException({'detail': 701})
            else:
                raise CustomAPIException({'detail': 700})
    else:
        raise CustomAPIException({'detail': 'First connection not found.'}, 404)

