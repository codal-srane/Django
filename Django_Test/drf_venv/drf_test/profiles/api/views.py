from django.contrib.auth.models import User
from .serializers import (
	UserLoginSerializer,
	UserCreateSerializer,
	UserChangePasswordSerializer,
	)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authentication import TokenAuthentication


class UserCreateAPIView(APIView):
	serializer_class = UserCreateSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserCreateSerializer(data = data)
		if serializer.is_valid(raise_exception = True):
			serializer.save()
			return Response({'message': 'New user created'}, status = HTTP_200_OK)
		return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data = data)
		if serializer.is_valid(raise_exception = True):
			validated_data = serializer.data
			del validated_data['username']
			return Response(validated_data, status = HTTP_200_OK)
		return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


class UserChangePasswordAPIView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = UserChangePasswordSerializer
	
	def put(self, request, *args, **kwargs):
		data = request.data
		serializer = UserChangePasswordSerializer(data = data)
		user_obj = User.objects.get(username = request.user)
		if serializer.is_valid(raise_exception = True):
			if user_obj.check_password(serializer.data['password']):
				user_obj.set_password(serializer.data['new_password'])
				user_obj.save()
				return Response({'message': 'Password has been changed'}, status = HTTP_200_OK)
			return Response({'message': 'Invalid Password'}, status = HTTP_200_OK)
		return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)