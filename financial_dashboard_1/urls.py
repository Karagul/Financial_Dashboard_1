"""financial_dashboard_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from dashapp.views import (
    HomePageView,
    TestTableView,
    TestFormView
)

urlpatterns = [
    re_path(r"^$", HomePageView.as_view(), name="home"),
    re_path(r"^test_table$", TestTableView.as_view(), name="test_table"),
    re_path(r"^test_form$", TestFormView.as_view(), name="test_form"),
]
