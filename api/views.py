from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.generics import ListAPIView
from . models import *
from . serializers import *

# Create your views here.

class HomeView(APIView):
    def get(self, request):
        return Response ({"message": "Hello"})
    
class SignUpView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        serializer = SignUpSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User sign up successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Sign up was unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class CheckSession(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            
            return Response({'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name}}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No active session"}, status=status.HTTP_401_UNAUTHORIZED)
        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": 'Login succesful', 'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login unsuccesful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": 'Logout succesful'},status=status.HTTP_204_NO_CONTENT)
    
class ClockInView(APIView):
    def post(self, request):
        serializer = TimeClockSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Clock in succesful', "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Clock in unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ClockOutView(APIView):
    def patch(self, request, id):
        time_clock = TimeClock.objects.get(id=id)
        serializer = TimeClockSerializer(time_clock, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Clock out successful', "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Clock out unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class TimeSheetView(ListAPIView):
    serializer_class = TimeClockSerializer

    def get_queryset(self):
        user = self.request.user
        return TimeClock.objects.filter(employee=user) 
        
        