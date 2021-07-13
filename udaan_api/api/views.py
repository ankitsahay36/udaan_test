# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from api.covid_orchestrator.covid_data_orchestrator import CovidController
# APIs:
# registerUser:
# Sample request - {"name":"A","phoneNumber":"9999999999","pinCode":"111111"}
# Sample response - {"userId": "1"}
# selfAssessment:
# Sample request - {"userId":"1","symptoms":["fever","cold","cough"],"travelHistory":true,"contactWithCovidPatient":true}
# Sample response - {"riskPercentage": 95}
covid_controller = CovidController()
success_status = 201
fail_status = 400

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def user_register(request):
    params = request.data
    try:
        if "name" not in params:
            raise Exception("name is missing in the request")
        if "phoneNumber" not in params:
            raise Exception("phoneNumber missing in the request")
        if "pinCode" not in params:
            raise Exception("pinCode missing in the request")
        user_register = covid_controller.register_user(params)
        return Response(user_register, status=success_status)

    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": fail_status}).data
        return Response(response, status=fail_status)

# {"userId":"1","symptoms":["fever","cold","cough"],"travelHistory":true,"contactWithCovidPatient":true}


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def user_risk(request):
    params = request.data
    try:
        if "userId" not in params:
            raise Exception("userId is missing in the request")
        if "symptoms" not in params:
            raise Exception("symptoms missing in the request")
        if "travelHistory" not in params:
            raise Exception("travelHistory missing in the request")
        if "contactWithCovidPatient" not in params:
            raise Exception("contactWithCovidPatient missing in the request")
        risk_check = covid_controller.risk_check(params)
        return Response(risk_check, status=success_status)

    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": fail_status}).data
        return Response(response, status=fail_status)

# registerAdmin:
# Sample request - {"name":"X","phoneNumber":"9999999999","pinCode":"111111"}
# Sample response - {"adminId": "2"}
# updateCovidResult:
# Sample request - {"userId":"1","adminId":"2","result":"positive"}
# Sample response - {"updated":true}


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def admin_register(request):
    params = request.data
    try:
        if "name" not in params:
            raise Exception("name is missing in the request")
        if "phoneNumber" not in params:
            raise Exception("phoneNumber missing in the request")
        if "pinCode" not in params:
            raise Exception("pinCode missing in the request")
        admin_register = covid_controller.register_admin(params)
        return Response(admin_register, status=success_status)

    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": fail_status}).data
        return Response(response, status=fail_status)

# {"userId":"1","adminId":"2","result":"positive"}
@api_view(["POST"])
@renderer_classes([JSONRenderer])
def admin_report(request):
    params = request.data
    try:
        if "userId" not in params:
            raise Exception("userId is missing in the request")
        if "adminId" not in params:
            raise Exception("adminId missing in the request")
        if "result" not in params:
            raise Exception("result missing in the request")
        admin_report = covid_controller.admin_report(params)
        return Response(admin_report, status=success_status)
    # {"userId": "1", "adminId": "2", "result": "positive"}
    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": fail_status}).data
        return Response(response, status=fail_status)


class ErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    code = serializers.CharField()


