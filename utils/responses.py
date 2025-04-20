from rest_framework.exceptions import APIException
from rest_framework.response import Response


class CustomException(APIException):
    status_code = 400
    default_detail = {'detail': 'Something went wrong!'}


success = Response(data={'detail': "Success!"}, status=200)
error = CustomException({'detail': "Xatolik yuz berdi"})
none = CustomException({'detail': "Kiritilganlar bo'yicha malumot topilmadi"})
value_e = CustomException({'detail': "Malumotlarni to'g'ri shakilda jo'nating"})
restricted = CustomException({'detail': "Bu amaliyot uchun sizda ruhsat mavjud emas"})


response_schema = {
    200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
    # 400: {"description": "The operation did not complete successfully", "example": {"response": "Bad Request!"}},
}
