from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import models
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
	confirm_password = serializers.CharField(write_only = True)
	class Meta:
		model = User
		fields =[
			'username',
			'email',
			'first_name',
			'last_name',
			'password',
			'confirm_password'
		]
		write_only_fields = ['password'] 

	def validate(self, data):
		if not data.get('email'):
			raise serializers.ValidationError("The email cannot be blank.")        
		if not data.get('password') or not data.get('confirm_password'):
			raise serializers.ValidationError("Please enter a password and "
                "confirm it.")
		if data.get('password') != data.get('confirm_password'):
			raise serializers.ValidationError("The passwords don't match.")
		return data

	def create(self, validated_data):
		password = validated_data.pop('password')
		validated_data.pop('confirm_password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		Token.objects.create(user=instance)
		return instance


class UserLoginSerializer(serializers.ModelSerializer):
	token = serializers.CharField(allow_blank = True, read_only = True)
	username = serializers.CharField()
	class Meta:
		model = User
		fields =[
			'id',
			'first_name',
			'last_name',
			'email',
			'username',
			'password',
			'token',
			]
		extra_kwargs = {
			'password': {'write_only': True},
			'first_name': {'read_only': True},
			'last_name': {'read_only': True},
			'email': {'read_only': True},
			'token': {'read_only': True}
			}

	def validate(self, data):
		username = data['username']
		password = data['password']
		user = User.objects.filter(
			models.Q(username = username)
			)
		if user.exists() and user.count() == 1:
			user_obj = user.first()
			if user_obj.check_password(password):
				data['token'] = Token.objects.filter(user=user_obj).first().key
				data['id'] = user_obj.id
				data['first_name'] = user_obj.first_name
				data['last_name'] = user_obj.last_name
				data['email'] = user_obj.email
				return data
			else:
				raise ValidationError('Incorrect Credentials.')
		else:
			raise ValidationError('The username is invalid.')