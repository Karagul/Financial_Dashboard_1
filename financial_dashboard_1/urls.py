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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from dashapp.views import (
    HomePageView,
    RevenuesView,
    LoginView,
    MainRegistrationView,
    MainPanelView,
    IncomeStatementView,
    logout_view
)

# ToDo: Na koniec uporządkować tą listę

urlpatterns = [

    # Main views

    re_path(r"^admin/", admin.site.urls),
    re_path(r"^$", HomePageView.as_view(), name="home"),

    # Login/registration views

    path("registration/", MainRegistrationView.as_view(), name="registration"),
    re_path(r"^login/$", LoginView.as_view(), name="login"),
    re_path(r"^logout/$", logout_view, name="logout"),

    # Company-specific views

    re_path(
        r"^(?P<pk>(\d)+)/main-panel/$",
        MainPanelView.as_view(),
        name="main-panel"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/revenues/$", RevenuesView.as_view(), name="revenues"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/income-statement/$",
        IncomeStatementView.as_view(),
        name="income-statement"
    ),

]
