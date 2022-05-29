from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .serializers import CustomUserSerializers
from .models import CustomUser, Like
from .utils import match, get_res, get_distance



def index(request):
    return render(request, 'index.html')


class UserCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializers

    def create(self, request, format=None):
        serializer = CustomUserSerializers(data=request.data)
        password = request.data['password']
        try:
            password_validation.validate_password(password)
            if serializer.is_valid():
                hashed_password = make_password(serializer.validated_data['password'])
                serializer.validated_data['password'] = hashed_password
                longitude, latitude = get_res(request)
                data = dict()
                data['f_name'] = serializer.validated_data['f_name']
                data['l_name'] = serializer.validated_data['l_name']
                data['email'] = serializer.validated_data['email']
                data['password'] = serializer.validated_data['password']
                data['avatar'] = serializer.validated_data['avatar']
                data['gender'] = serializer.validated_data['gender']
                data['longitude'] = longitude
                data['latitude'] = latitude

                CustomUser.objects.create(**data)

        except Exception as err:
            return Response(f'Retype password {err}', status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_201_CREATED)


class UserFilter(filters.FilterSet):
    def distance_filter(qs, name, value):
        return qs

    distance = filters.NumberFilter(field_name='distance', label='дистанция', method=distance_filter)

    class Meta:
        model = CustomUser
        fields = ('gender', 'f_name', 'l_name')

    @property
    def qs(self):
        queryset = super().qs
        if self.data.get('distance'):
            distance = float(self.data.get('distance'))
            data = list()
            lon1 = self.request.user.longitude
            lat1 = self.request.user.latitude
            for user in CustomUser.objects.all():
                lon2 = user.longitude
                lat2 = user.latitude
                if get_distance(lon1, lat1, lon2, lat2) <= distance:
                    data.append(user.email)
            result_query = queryset.filter(email__in=data)
            return result_query
        else:
            return queryset


class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializers
    filter_backends = [DjangoFilterBackend]
    filter_class = UserFilter


@api_view(['GET'])
def create_like(request, pk):
    try:
        user_to = CustomUser.objects.get(id=pk)
        user = request.user
        data = dict()
        data["user"] = user
        data["user_to"] = user_to
        Like.objects.create(**data)
        result_str = match(user, user_to)
    except Exception as err:
        return Response(f"{err}", status=status.HTTP_404_NOT_FOUND)
    return Response(f"{result_str}", status=status.HTTP_200_OK)
