"""shop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import (
    IndexListView,
    ProductsListView,
    DeleteProductView,
    ProductDetailView,
    AddProductView,
    CartView,
    MakeOrderView,
)

urlpatterns = [
    url(r'^cart/order/', MakeOrderView.as_view(), name='make_order'),
    url(r'^cart/', CartView.as_view(), name='cart'),
    url(r'^$', IndexListView.as_view(), name='main'),
    url(r'^(\d+)/$', ProductsListView.as_view(), name='products-list'),
    url(r'^(\d+)/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    url(r'^add_product/$', AddProductView.as_view()),
    url(r'^delete_product/(?P<pk>\d+)/$', DeleteProductView.as_view()),
]
