from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from dashapp.forms import TestForm1
from dashapp.models import Revenue, Cost, Employee, Customer, Procedure,\
    Country, PaymentType, Project, Currency, CostCategory


class HomePageView(TemplateView):
    template_name = "home.html"


class RevenuesView(TemplateView):
    # Tabela mogłaby wyświetlać tylko część danych, a reszta w popupie po naciśnięciu?
    template_name = "revenues.html"

    def get_context_data(self, **kwargs):
        return {"revenues" : Revenue.objects.all().order_by("document_date")}


class TestFormView(FormView):
    template_name = "form.html"
    form_class = TestForm1


class LoginView(TemplateView):
    # Alternatywnie modal?
    template_name = ""


class RegistrationView(TemplateView):
    template_name = ""

class EmployeePanelView(TemplateView):
    template_name = "employee_panel.html"

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
