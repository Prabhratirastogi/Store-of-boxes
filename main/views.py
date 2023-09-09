from rest_framework import generics,permissions, status, serializers
from .models import Box
from django.db.models import Avg
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BoxListSerializer, BoxCreateSerializer, BoxUpdateSerializer, UserSerializer, BoxDeleteSerializer
from django.contrib.auth.hashers import make_password
from django.utils.timezone import datetime, timedelta
from django.conf import settings


average_area_limit = settings.A1
total_boxes_added_limit = settings.L1
total_boxes_added_by_user_limit = settings.L2
average_volume_limit = settings.V1

class BoxListView(generics.ListAPIView):
    serializer_class = BoxListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get_queryset(self):
        queryset = Box.objects.all()

        # Filter boxes created by a specific user by username
        created_by_username = self.request.query_params.get('created_by_username')
        if created_by_username:
            queryset = queryset.filter(created_by__username=created_by_username)

        # Apply filters for length, width, height, area, and volume
        length_more_than = self.request.query_params.get('length_more_than')
        length_less_than = self.request.query_params.get('length_less_than')
        breadth_more_than = self.request.query_params.get('breadth_more_than')
        breadth_less_than = self.request.query_params.get('breadth_less_than')
        height_more_than = self.request.query_params.get('height_more_than')
        height_less_than = self.request.query_params.get('height_less_than')
        area_more_than = self.request.query_params.get('area_more_than')
        area_less_than = self.request.query_params.get('area_less_than')
        volume_more_than = self.request.query_params.get('volume_more_than')
        volume_less_than = self.request.query_params.get('volume_less_than')

        if length_more_than is not None:
            queryset = queryset.filter(length__gt=length_more_than)
        if length_less_than is not None:
            queryset = queryset.filter(length__lt=length_less_than)
        if breadth_more_than is not None:
            queryset = queryset.filter(width__gt=breadth_more_than)
        if breadth_less_than is not None:
            queryset = queryset.filter(width__lt=breadth_less_than)
        if height_more_than is not None:
            queryset = queryset.filter(height__gt=height_more_than)
        if height_less_than is not None:
            queryset = queryset.filter(height__lt=height_less_than)
        if area_more_than is not None:
            queryset = queryset.filter(length__width__gt=area_more_than)
        if area_less_than is not None:
            queryset = queryset.filter(length__width__lt=area_less_than)
        if volume_more_than is not None:
            queryset = queryset.filter(length__width__height__gt=volume_more_than)
        if volume_less_than is not None:
            queryset = queryset.filter(length__width__height__lt=volume_less_than)

        return queryset

# Create View
class BoxCreateView(generics.CreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxCreateSerializer

    def perform_create(self, serializer):
        # Check the average volume of boxes added by the current user
        user = self.request.user
        average_volume = Box.objects.filter(created_by=user).aggregate(avg_volume=Avg('length' * 'width' * 'height'))['avg_volume']
        if average_volume is not None and average_volume + (self.request.data['length'] * self.request.data['width'] * self.request.data['height']) > average_volume_limit :
            raise serializers.ValidationError("Average volume exceeds the limit.")

        # Check the average area of boxes added by the current user
        average_area = Box.objects.filter(created_by=user).aggregate(avg_area=Avg('length' * 'width'))['avg_area']
        if average_area is not None and average_area + (self.request.data['length'] * self.request.data['width']) > average_area_limit:
            raise serializers.ValidationError("Average area exceeds the limit.")

        # Check the total number of boxes added in the current week
        current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        current_week_end = current_week_start + timedelta(days=6)
        total_boxes_in_week = Box.objects.filter(created_by=user, created_at__range=[current_week_start, current_week_end]).count()
        if total_boxes_in_week >= total_boxes_added_limit :
            raise serializers.ValidationError("Total boxes added in the current week exceeds the limit.")

        # Check the total number of boxes added in the current week by the user
        total_boxes_in_week_by_user = Box.objects.filter(created_by=user, created_at__range=[current_week_start, current_week_end]).count()
        if total_boxes_in_week_by_user >= total_boxes_added_by_user_limit:
            raise serializers.ValidationError("Total boxes added in the current week by the user exceeds the limit.")

        # Automatically associate the logged-in user as the creator
        serializer.save(created_by=user)

    def get_permissions(self):
        #  check if the user is staff
         if self.request.user.is_staff:
            # Allow staff members to add boxes
            return [permissions.IsAuthenticated()]
         else:
            # Disallow non-staff members from adding boxes
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
         
# Box Update view
class BoxUpdateView(generics.UpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        # Get the box object to be updated
        instance = self.get_object()

        # Check the average volume of boxes added by the current user
        user = self.request.user
        average_volume = Box.objects.filter(created_by=user).exclude(pk=instance.pk).aggregate(avg_volume=Avg('length' * 'width' * 'height'))['avg_volume']
        if average_volume is not None and average_volume + (request.data['length'] * request.data['width'] * request.data['height']) > average_volume_limit:
            raise serializers.ValidationError("Average volume exceeds the limit.")

        # Check the average area of boxes added by the current user
        average_area = Box.objects.filter(created_by=user).exclude(pk=instance.pk).aggregate(avg_area=Avg('length' * 'width'))['avg_area']
        if average_area is not None and average_area + (request.data['length'] * request.data['width']) > average_area_limit:
            raise serializers.ValidationError("Average area exceeds the limit.")

        # Check the total number of boxes added in the current week
        current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        current_week_end = current_week_start + timedelta(days=6)
        total_boxes_in_week = Box.objects.filter(created_by=user, created_at__range=[current_week_start, current_week_end]).exclude(pk=instance.pk).count()
        if total_boxes_in_week >= total_boxes_added_limit:
            raise serializers.ValidationError("Total boxes added in the current week exceeds the limit.")

        # Check the total number of boxes added in the current week by the user
        total_boxes_in_week_by_user = Box.objects.filter(created_by=user, created_at__range=[current_week_start, current_week_end]).exclude(pk=instance.pk).count()
        if total_boxes_in_week_by_user >= total_boxes_added_by_user_limit:
            raise serializers.ValidationError("Total boxes added in the current week by the user exceeds the limit.")

        # Update the box object
        return super().update(request, *args, **kwargs)




class RegisterUser(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
               # Hash the user's password before saving it
            password = serializer.validated_data['password']
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # Call the parent class's post method to handle authentication
        response = super().post(request, *args, **kwargs)
        
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # Generate or retrieve a token for the user
            token, created = Token.objects.get_or_create(user=request.user)
            response.data['token'] = token.key
            return response

        return response
    
class BoxDeleteView(generics.DestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        box = self.get_object()  # Get the box object using DRF's get_object method

        # Check if the authenticated user is the creator of the box
        if box.created_by != request.user:
            return Response({"detail": "You are not allowed to delete this box."}, status=status.HTTP_403_FORBIDDEN)

        box.delete()  # Delete the box

        return Response(status=status.HTTP_204_NO_CONTENT)