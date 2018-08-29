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
    CashFlowView,
    RevenuesView,
    ExpensesView,
    LoginView,
    MainRegistrationView,
    MainDashboardView,
    ManagerDashboardView,
    ModificationDashboardView,
    IncomeStatementView,
    logout_view,
    NewEmployeeRegistrationView,
    RevenueModifyView,
    ExpenseModifyView,
)

# ToDo: Na koniec uporządkować tą listę

urlpatterns = [

    # Main views

    re_path(r"^admin/", admin.site.urls),
    re_path(r"^$", HomePageView.as_view(), name="home"),

    # Login/registration views

    path("registration/", MainRegistrationView.as_view(), name="registration"),
    re_path(r"^login/?$", LoginView.as_view(), name="login"),
    re_path(r"^logout/?$", logout_view, name="logout"),

    # Company-specific views

    # Employee views

    re_path(
        r"^(?P<pk>(\d)+)/main-dashboard/?$",
        MainDashboardView.as_view(),
        name="main-dashboard"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/revenues/?$", RevenuesView.as_view(), name="revenues"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/expsenes/?$", ExpensesView.as_view(), name="expenses"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/company-settings/?$",
        ModificationDashboardView.as_view(),
        name="company-settings"
    ),
    re_path(
        r"^revenue-modify/(?P<pk>(\d)+)/?$",
        RevenueModifyView.as_view(),
        name="revenue-modify"
    ),
    re_path(
        r"^expense-modify/(?P<pk>(\d)+)/?$",
        ExpenseModifyView.as_view(),
        name="expense-modify"
    ),

    # Manager views

    re_path(
        r"^(?P<pk>(\d)+)/manager-dashboard/?$",
        ManagerDashboardView.as_view(),
        name="manager-dashboard"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/income-statement/?$",
        IncomeStatementView.as_view(),
        name="income-statement"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/cash-flow/?$",
        CashFlowView.as_view(),
        name="cash-flow"
    ),
    re_path(
        r"^(?P<pk>(\d)+)/new-employee/?$",
        NewEmployeeRegistrationView.as_view(),
        name="new-employee"
    ),


]
