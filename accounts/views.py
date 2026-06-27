from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data
        
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()
        
        profile = user.profile
        
        # Profile fields could be nested (if JSON) or flat (if FormData)
        profile_data = data.get('profile', {}) if isinstance(data.get('profile'), dict) else {}
        
        def get_field(key, default):
            val = data.get(key)
            if val is None and key in profile_data:
                val = profile_data.get(key)
            return val if val is not None else default

        profile.phone_number = get_field('phone_number', profile.phone_number)
        profile.city = get_field('city', profile.city)
        
        dob = get_field('date_of_birth', None)
        if dob is not None:
            if dob in ['', 'null', 'None', 'undefined']:
                profile.date_of_birth = None
            else:
                profile.date_of_birth = dob
                
        address = get_field('address', None)
        if address is not None:
            if address in ['', 'null', 'None', 'undefined']:
                profile.address = None
            else:
                profile.address = address
                
        state = get_field('state', None)
        if state is not None:
            if state in ['', 'null', 'None', 'undefined']:
                profile.state = None
            else:
                profile.state = state

        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        elif 'profile_photo' in data:
            if data['profile_photo'] in ['', 'null', 'None', None]:
                profile.profile_photo = None
                
        profile.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


from rest_framework.permissions import IsAdminUser

class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('username')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
