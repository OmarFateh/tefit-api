from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(serializers.ModelSerializer):
    """
    A user serializer.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ('username',)


class UserCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for user registeration.
    """
    email = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm Email')
    password2 = serializers.CharField(
        label='Confirm Password', write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'email2',
                  'password', 'password2']
        extra_kwargs = {"password": {'write_only': True}}

    def validate_email(self, value):
        """
        Validate email 1.
        """
        data = self.get_initial()
        email1 = value
        email2 = data.get('email2')
        # check if the two emails match.
        if email1 != email2:
            raise serializers.ValidationError('The two Emails must match.')
        # check if the email has already been used.
        if User.objects.filter(email=email1).exists():
            raise serializers.ValidationError(
                "An account with this Email already exists.")
        return value

    def validate_password(self, value):
        """
        Validate passwords.
        """
        data = self.get_initial()
        password1 = value
        password2 = data.get('password2')
        # check if the two passwords match
        if password1 != password2:
            raise serializers.ValidationError('The two Passwords must match.')
        return value

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(username=username, first_name=first_name,
                        last_name=last_name, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    """
    A serializer for user login.
    """
    username_email = serializers.CharField(label='Username or Email')
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username_email', 'password', 'token']
        extra_kwargs = {"password": {'write_only': True}}

    def get_token(self, obj):
        request = self.context['request']
        refresh = RefreshToken.for_user(request.user)
        response = {'refresh': str(refresh), 'access': str(
            refresh.access_token), }
        return response

    def validate(self, data):
        """
        Validate entered data.
        """
        request = self.context['request']
        username_email = data.get("username_email", None)
        password = data["password"]
        # check if the entered username or email and password are correct.
        user = authenticate(username=username_email, password=password)
        # Username or Email and Password are correct.
        if user:
            # login user.
            login(request, user)
        else:
            raise serializers.ValidationError(
                "Username or Password is incorrect.")
        return data


class UserLogoutSerializer(serializers.Serializer):
    """
    A serializer for user logout.
    """
    refresh_token = serializers.CharField(label='Refresh Token')

    def validate(self, data):
        """
        Validate entered data.
        """
        request = self.context['request']
        refresh_token = data.get("refresh_token", None)
        # check if the entered token is valid and add it to blacklist.
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError as e:
            raise serializers.ValidationError("Token is invalid or expired.")
        return data


class PassowordChangeSerializer(serializers.ModelSerializer):
    """
    A serializer for password change.
    """
    old_password = serializers.CharField(label='Old Password', write_only=True)
    new_password1 = serializers.CharField(
        label='New Password', write_only=True)
    new_password2 = serializers.CharField(
        label='Confirm New Password', write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def validate_old_password(self, value):
        """
        Validate old password.
        """
        request = self.context['request']
        # check if the password is correct
        if not request.user.check_password(value):
            raise serializers.ValidationError("Password is incorrect.")
        return value

    def validate_new_password1(self, value):
        """
        Validate passwords.
        """
        data = self.get_initial()
        password1 = value
        password2 = data.get('new_password2')
        # check if the two passwords match
        if password1 != password2:
            raise serializers.ValidationError('The two Passwords must match.')
        return value

    def update(self, instance, validated_data):
        """
        Update user's password.
        """
        password = validated_data['new_password1']
        instance.set_password(password)
        instance.save()
        return validated_data


class PasswordResetEmailSerializer(serializers.Serializer):
    """
    Password reset email serializer.
    """
    email = serializers.EmailField(label='Email Address')

    class Meta:
        fields = ['email']

    def validate_email(self, value):
        """
        Validate entered data.
        """
        request = self.context['request']
        email = value
        # check if the entered email is correct.
        if not User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email is incorrect.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """
    Password reset serializer.
    """
    new_password1 = serializers.CharField(
        label='New Password', write_only=True)
    new_password2 = serializers.CharField(
        label='Confirm New Password', write_only=True)
    token = serializers.CharField(label='Token', write_only=True)
    uidb64 = serializers.CharField(label='UIDB64', write_only=True)

    class Meta:
        fields = ['new_password1', 'new_password2', 'token', 'uidb64']

    def validate_new_password1(self, value):
        """
        Validate passwords.
        """
        data = self.get_initial()
        password1 = value
        password2 = data.get('new_password2')
        # check if the two passwords match
        if password1 != password2:
            raise serializers.ValidationError('The two Passwords must match.')
        return value

    def validate(self, data):
        """
        Validate entered data.
        """
        try:
            password = data.get("new_password1")
            token = data.get("token")
            uidb64 = data.get("uidb64")
            # get user by id.
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=user_id)
            # check if the token is valid.
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid.', 401)
            # set new password
            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed('The reset link is invalid.', 401)
        return data
