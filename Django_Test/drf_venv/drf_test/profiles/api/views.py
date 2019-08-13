from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import (
	UserLoginSerializer,
	UserCreateSerializer,
	)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class UserCreateAPIView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer


class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data = data)
		if serializer.is_valid(raise_exception = True):
			validated_data = serializer.data
			del validated_data['username']
			return Response(validated_data, status = HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)