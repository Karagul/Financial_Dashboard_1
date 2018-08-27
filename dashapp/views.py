from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import request, HttpRequest
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from dashapp.forms import LoginForm, UserRegisterForm, CompanyRegisterForm
from dashapp.models import Revenue, Cost, Employee, Customer, Procedure, \
    Country, PaymentType, Project, Currency, CostCategory, Company, \
    CompanyMember
from dashapp.mixins import GroupRequiredMixin


# Main views

class HomePageView(TemplateView):
    template_name = "home.html"


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    # ToDo: should send user back to main page? Or to the panel perhaps?
    success_url = ""
    # success_url = reverse_lazy("main-panel", kwargs=request.user.companymember.company.id)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["login"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(self.request, user)
            self.success_url = reverse_lazy(
                "main-panel", kwargs={"pk": user.companymember.company.id}
            )
            return super(LoginView, self).form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                error="No user exists with that username."
            )), user

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
                form=form,
                error="Wrong login or password."
            ))

def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


class MainRegistrationView(View):
    def get(self, request):
        return TemplateResponse(
            request, "registration.html", {
                "form_company": CompanyRegisterForm,
                "form_manager": UserRegisterForm
            }
        )

    def post(self, request):
        form_company = CompanyRegisterForm(request.POST)
        form_manager = UserRegisterForm(request.POST)
        if form_company.is_valid() and form_manager.is_valid():

            # Check if passwords match each other
            if form_manager.cleaned_data["password"]\
                != form_manager.cleaned_data["password_repeated"]:
                return TemplateResponse(
                    request, "registration.html", {
                        "form_company": form_company,
                        "form_manager": form_manager,
                        "error": "Passwords do not match."
                    }
                )

            # Create a new company
            new_company = form_company.save()

            # Create a new manager-user
            new_user = User.objects.create_user(
                username=form_manager.cleaned_data["username"],
                password=form_manager.cleaned_data["password"],
                email=form_manager.cleaned_data["email"],
                first_name=form_manager.cleaned_data["first_name"],
                last_name=form_manager.cleaned_data["last_name"],
            )
            CompanyMember.objects.create(
                company=new_company,
                user=new_user
            )

            # Create a new group for this company, using its pk
            new_group = Group.objects.create(
                name=("company_" + new_company.pk)
            )
            # ToDo: Check if current no-permission solution is sufficient.
            # Employee needs only a company group. And manager the manager
            # group and the company group


            # Add user to groups
            new_group.user_set.add(new_user)
            Group.objects.get(pk=2).user_set.add(new_user)

            # When done, hide groups in form


            login(request, new_user)
            return redirect(
                reverse("main-panel", kwargs={"pk": new_company.id})
            )
        else:
            return TemplateResponse(
            request, "registration.html", {
                "form_company": form_company,
                "form_manager": form_manager
            }
        )



class MainPanelView(LoginRequiredMixin, TemplateView):
    template_name = "main_panel.html"


# Employee views
# ToDo: Some views could be ListViews?

class RevenuesView(LoginRequiredMixin,TemplateView):
    # Tabela mogłaby wyświetlać tylko część danych, a reszta w popupie po naciśnięciu?
    template_name = "revenues.html"

    def get_context_data(self, **kwargs):
        return {"revenues" : Revenue.objects.all().order_by("document_date")}


# Manager views

class IncomeStatementView(
    LoginRequiredMixin, GroupRequiredMixin, TemplateView
):

    # Checks for employee-type group, the company group is checked within the
    # custom mixin GroupRequiredMixin
    group_required = ["Managers"]


    # def get_group_required(self):
    #     return self.request.user.companymember.company.id

    # group_required = ["Managers", "company_" + request.user.companymember.company.id]



    # ToDo: Currently counts total revenues
    template_name = "income_statement.html"

    # ToDo: Dodać filtrowanie po id firmy, później po okresie - od początku roku
    revenue_data = Revenue.objects.all()
    total_net_revenues = 0
    # ToDo: Zaokrąglić
    for revenue in revenue_data:
        total_net_revenues += revenue.net_amount_converted

    def get_context_data(self, **kwargs):
        return {"total_net_revenues" : self.total_net_revenues}
