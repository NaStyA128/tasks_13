from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    MyUserSerializer,
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderProductsSerializer
)
from .models import (
    MyUser,
    Category,
    Product,
    Order,
    OrderProducts
)

# Create your views here.


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderProductsViewSet(viewsets.ModelViewSet):
    queryset = OrderProducts.objects.all()
    serializer_class = OrderProductsSerializer


# class BlaViewSet(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, format=None):
#         content = {
#             'user': request.user,  # `django.contrib.auth.User` instance.
#             'auth': request.auth,  # None
#         }
#         return Response(content)
