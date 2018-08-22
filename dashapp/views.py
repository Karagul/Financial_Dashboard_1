from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView
from dashapp.forms import TestForm1, LoginForm
from dashapp.models import Revenue, Cost, Employee, Customer, Procedure,\
    Country, PaymentType, Project, Currency, CostCategory


# Main views

class HomePageView(TemplateView):
    template_name = "home.html"


class LoginView(FormView):
    # Alternatywnie modal?
    template_name = "login.html"
    form_class = LoginForm
    # ToDo: should send user back to main page? Or to the panel perhaps?
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["login"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                error="No user exists with that username."
            ))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
                form=form,
                error="Wrong login or password."
            ))

def logout_view(request):
    logout(request)
    return redirect(reverse("/"))


class RegistrationView(TemplateView):
    template_name = ""


class EmployeePanelView(TemplateView):
    template_name = "employee_panel.html"


# Employee views

class RevenuesView(TemplateView):
    # Tabela mogłaby wyświetlać tylko część danych, a reszta w popupie po naciśnięciu?
    template_name = "revenues.html"

    def get_context_data(self, **kwargs):
        return {"revenues" : Revenue.objects.all().order_by("document_date")}


# Manager views

class IncomeStatementView(TemplateView):
    # ToDo: Currently counts total revenues
    template_name = "income_statement.html"

    # ToDo: Dodać filtrowanie po id firmy, później po okresie - od początku roku
    revenue_data = Revenue.objects.all()
    total_net_revenues = 0
    # ToDo: Zaokrąglić
    for revenue in revenue_data:
        total_net_revenues += revenue.net_amount_foreign * revenue.exchange_rate

    def get_context_data(self, **kwargs):
        return {"total_net_revenues" : self.total_net_revenues}


# Test views

class TestFormView(FormView):
    template_name = "form.html"
    form_class = TestForm1
