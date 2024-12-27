from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import RegisterSerializer
from users.models import User
import random
from users.utils import send_otp
from users.models import OTP


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # GENERATE OTP
            otp = str(random.randint(100000, 999999))
            phone_number = serializer.data['phone_number']

            # STORE OTP
            OTP.objects.create(phone_number=phone_number, otp=otp)

            # SEND SMS
            send_otp(phone_number, otp)
            return Response({"message": "User registered successfully. OTP sent!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        otp_obj = OTP.objects.filter(phone_number=phone_number).order_by('-created_time').first()
        if otp_obj and otp_obj.is_valid() and otp_obj.otp == otp:
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "User not registered"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
