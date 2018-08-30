from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import request, HttpResponseForbidden
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, UpdateView, CreateView
from dashapp.forms import LoginForm, UserRegisterForm, CompanyRegisterForm, \
    AddRevenueForm, EmployeeRegisterForm, ModifyRevenueForm, ModifyExpenseForm, \
    AddExpenseForm
from dashapp.models import Revenue, Expense, Employee, Customer, Procedure, \
    Country, PaymentType, Project, Currency, ExpenseCategory, Company, \
    CompanyMember
import datetime
import calendar
from decimal import *

# ToDo: Maybe move those functions somewhere else?

def revenue_calculator(company_id, start_date, end_date):
    data = Revenue.objects.filter(
        company=company_id,
        document_date__range=[start_date, end_date]
    )
    total = 0
    for revenue in data:
        total += revenue.net_amount_converted
    return total


def expense_calculator(company_id, start_date, end_date):
    data = Expense.objects.filter(
        company=company_id,
        document_date__range=[start_date, end_date]
    )
    total = 0
    for revenue in data:
        total += revenue.net_amount
    return total

def receipt_calculator(company_id, start_date, end_date):
    data = Revenue.objects.filter(
        company=company_id,
        settlement_status=True,
        actual_payment_date__range=[start_date, end_date]
    )
    total = 0
    for receipt in data:
        total += receipt.gross_amount_converted
    return total

def expenditure_calculator(company_id, start_date, end_date):
    data = Expense.objects.filter(
        company=company_id,
        settlement_status=True,
        actual_payment_date__range=[start_date, end_date]
    )
    total = 0
    for expenditure in data:
        total += expenditure.gross_amount
    return total


# Views begin here

class HomePageView(TemplateView):
    template_name = "home.html"


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = ""

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["login"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(
                self.request, user
            )
            self.success_url = reverse_lazy(
                "main-dashboard", kwargs={"pk": user.companymember.company.id}
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

            # Create a new manager-user and link to extended User-class
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
            Group.objects.create(name=("company_" + str(new_company.pk)))

            # Add user to groups
            Group.objects.get(pk=2).user_set.add(new_user)

            login(request, new_user)
            return redirect(
                reverse("main-dashboard", kwargs={"pk": new_company.id})
            )
        else:
            return TemplateResponse(
            request, "registration.html", {
                "form_company": form_company,
                "form_manager": form_manager
            }
        )


class NewEmployeeRegistrationView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):

        user_groups = [
            group for group in request.user.groups.values_list(
                'name', flat=True
            )
        ]

        if str(request.user.companymember.company.id) == self.kwargs["pk"]\
                and "Managers" in user_groups:
            return super(NewEmployeeRegistrationView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def get(self, request, pk):
        return TemplateResponse(
            request, "employee_registration.html", {
                "form_employee": EmployeeRegisterForm
            }
        )

    def post(self, request, pk):
        form = EmployeeRegisterForm(request.POST)

        if form.is_valid() and form.is_valid():

            # ToDo: Generate a password for user and send it via e-mail
            # ToDo: Then the user should be able to change it at the 1st login
            #send_mail()
            password = "temporary"

            # Create a new user
            new_user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=password,
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )

            CompanyMember.objects.create(
                company=Company.objects.get(pk=pk),
                user=new_user
            )

            # Add user to the company group
            Group.objects.get(
                pk=form.cleaned_data["group"]
            ).user_set.add(new_user)

            return redirect(
                reverse("manager-dashboard",
                        kwargs={"pk": pk})
            )
        else:
            return TemplateResponse(
                request, reverse("new-employee", kwargs={"pk": pk}), {
                    "form_employee": form,
                }
        )


# Dashboard views

class MainDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "main_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.companymember.company.id) == self.kwargs["pk"]:

            return super(MainDashboardView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')


    def get_context_data(self, **kwargs):

        company_id = self.kwargs["pk"]

        # Date calculations
        today = datetime.date.today()
        current_year_beginning = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        current_month_beginning = today.replace(day=1)
        current_month_end = today.replace(
            day=calendar.monthrange(today.year, today.month)[1]
        )
        one_month_ago_beginning = (current_month_beginning
                                   - datetime.timedelta(days=1)).replace(day=1)
        one_month_ago_end = current_month_beginning \
                            - datetime.timedelta(days=1)

        return {
            "current_month_revenues": revenue_calculator(
                company_id,
                current_month_beginning,
                current_month_end
            ),
            "last_month_revenues": revenue_calculator(
                company_id,
                one_month_ago_beginning,
                one_month_ago_end
            ),
            "annual_revenues": revenue_calculator(
                company_id,
                current_year_beginning,
                current_year_end
            ),
            "current_month_expenses": expense_calculator(
                company_id,
                current_month_beginning,
                current_month_end
            ),
            "last_month_expenses": expense_calculator(
                company_id,
                one_month_ago_beginning,
                one_month_ago_end
            ),
            "annual_expenses": expense_calculator(
                company_id,
                current_year_beginning,
                current_year_end
            ),
        }


class ManagerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "manager_dashboard.html"

    def dispatch(self, request, *args, **kwargs):

        user_groups = [
            group for group in request.user.groups.values_list(
                'name', flat=True
            )
        ]

        if str(request.user.companymember.company.id) == self.kwargs["pk"]\
                and "Managers" in user_groups:
            return super(ManagerDashboardView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def get_context_data(self, **kwargs):

        company_id = self.kwargs["pk"]

        # Date calculations
        today = datetime.date.today()
        current_year_beginning = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        current_month_beginning = today.replace(day=1)
        current_month_end = today.replace(
            day=calendar.monthrange(today.year, today.month)[1]
        )

        revenues = revenue_calculator(
            company_id,
            current_year_beginning,
            current_year_end
            )

        expenses = expense_calculator(
            company_id,
            current_year_beginning,
            current_year_end
            )

        # ToDo: Tax rate should come from global company settings
        net = round((revenues - expenses) / Decimal(1.19), 2)\
            if revenues > expenses else revenues - expenses

        receipts = receipt_calculator(
            company_id,
            current_year_beginning,
            current_year_end
            )

        expenditures = expenditure_calculator(
            company_id,
            current_year_beginning,
            current_year_end
        )

        cash_change = receipts - expenditures

        return {
            "annual_revenue": revenues,
            "annual_expenses": expenses,
            "annual_net": net,
            "annual_receipts": receipts,
            "annual_expenditures": expenditures,
            "annual_cash_change": cash_change
        }

class RevenuesView(LoginRequiredMixin,TemplateView):

    template_name = "revenues.html"

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.companymember.company.id) == self.kwargs["pk"]:

            return super(RevenuesView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def get_context_data(self, **kwargs):

        # ToDo: To powinno wyświetlać ileśtam najnowszych + filtry

        return {
            "revenues" : Revenue.objects.filter(
                company=self.kwargs["pk"]
            ).order_by("document_date"),
            "revenue_form": AddRevenueForm
        }



class ExpensesView(LoginRequiredMixin, TemplateView):

    template_name = "expenses.html"

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.companymember.company.id) == self.kwargs["pk"]:

            return super(ExpensesView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def get_context_data(self, **kwargs):
        return {
            "expenses": Expense.objects.all().order_by("document_date"),
            "expense_form": AddExpenseForm
        }

# Manager views

class IncomeStatementView(
    LoginRequiredMixin, TemplateView
):
    template_name = "income_statement.html"

    def dispatch(self, request, *args, **kwargs):

        user_groups = [
            group for group in request.user.groups.values_list(
                'name', flat=True
            )
        ]

        if str(request.user.companymember.company.id) == self.kwargs["pk"]\
                and "Managers" in user_groups:
            return super(IncomeStatementView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')


    def get_context_data(self, **kwargs):

        # ToDo: Add filtering
        
        # ToDo: Covert calculations into a list perhaps

        company_id = self.kwargs["pk"]

        # Date calculations
        today = datetime.date.today()
        current_year_beginning = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        current_month_beginning = today.replace(day=1)
        current_month_end = today.replace(
            day=calendar.monthrange(today.year, today.month)[1]
        )
        one_month_ago_beginning = (current_month_beginning
                                   - datetime.timedelta(days=1)).replace(day=1)
        one_month_ago_end = current_month_beginning \
                            - datetime.timedelta(days=1)
        two_month_ago_beginning = (one_month_ago_beginning
                                   - datetime.timedelta(days=1)).replace(day=1)
        two_month_ago_end = one_month_ago_beginning \
                            - datetime.timedelta(days=1)
        three_month_ago_beginning = (two_month_ago_beginning
                                   - datetime.timedelta(days=1)).replace(day=1)
        three_month_ago_end = two_month_ago_beginning \
                            - datetime.timedelta(days=1)
        four_month_ago_beginning = (three_month_ago_beginning
                                   - datetime.timedelta(days=1)).replace(day=1)
        four_month_ago_end = three_month_ago_beginning \
                            - datetime.timedelta(days=1)
        five_month_ago_beginning = (four_month_ago_beginning
                                   - datetime.timedelta(days=1)).replace(day=1)
        five_month_ago_end = four_month_ago_beginning \
                            - datetime.timedelta(days=1)

        period_dictionary = {
            "year": [current_year_beginning, current_year_end],
            "0": [current_month_beginning, current_month_end],
            "-1": [one_month_ago_beginning, one_month_ago_end],
            "-2": [two_month_ago_beginning, two_month_ago_end],
            "-3": [three_month_ago_beginning, three_month_ago_end],
            "-4": [four_month_ago_beginning, four_month_ago_end],
            "-5": [five_month_ago_beginning, five_month_ago_end]
        }

        month_list = [
            calendar.month_name[five_month_ago_beginning.month],
            calendar.month_name[four_month_ago_beginning.month],
            calendar.month_name[three_month_ago_beginning.month],
            calendar.month_name[two_month_ago_beginning.month],
            calendar.month_name[one_month_ago_beginning.month],
            calendar.month_name[today.month]
        ]

        revenue_list = [
            revenue_calculator(company_id, v[0], v[1])
            for v in period_dictionary.values()
        ]
        expense_list = [
            expense_calculator(company_id, v[0], v[1])
            for v in period_dictionary.values()
        ]
        gross_profit_list = [
            revenue_list[i] - expense_list[i] for i in range(len(revenue_list))
        ]

        # ToDo: take tax rate from a global company setting
        tax_list = [
            round(gross_profit_list[i] * Decimal(0.19), 2)
            if revenue_list[i] > expense_list[i] else Decimal(0.00)
            for i in range(len(gross_profit_list))
        ]

        net_profit_list = [
            gross_profit_list[i] - tax_list[i]
            for i in range(len(gross_profit_list))
        ]

        return {
            "months": month_list,
            "total_net_revenues" : revenue_list.pop(0),
            "revenue_list": reversed(revenue_list),
            "total_net_expenses": expense_list.pop(0),
            "expense_list": reversed(expense_list),
            "total_gross_profit": gross_profit_list.pop(0),
            "gross_profit_list": reversed(gross_profit_list),
            "total_tax": tax_list.pop(0),
            "tax_list": reversed(tax_list),
            "total_net_profit": net_profit_list.pop(0),
            "net_profit_list": reversed(net_profit_list),
        }


class CashFlowView(
    LoginRequiredMixin, TemplateView
):
    template_name = "cash_flow.html"

    def dispatch(self, request, *args, **kwargs):

        user_groups = [
            group for group in request.user.groups.values_list(
                'name', flat=True
            )
        ]

        if str(request.user.companymember.company.id) == self.kwargs["pk"]\
                and "Managers" in user_groups:
            return super(CashFlowView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')


    def get_context_data(self, **kwargs):
        # ToDo: Currently counts total revenues

        # ToDo: Add filtering

        company_id = self.kwargs["pk"]

        # Date calculations
        today = datetime.date.today()
        current_year_beginning = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)

        return {
            "total_gross_receipts": receipt_calculator(
                company_id,
                current_year_beginning,
                current_year_end
            )
        }

class ModificationDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "modification_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.companymember.company.id) == self.kwargs["pk"]:

            return super(ModificationDashboardView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

# w Add pk to firma

class AddRevenueView(LoginRequiredMixin, CreateView):
    model = Revenue
    form_class = AddRevenueForm
    success_url = ""

    def dispatch(self, request, *args, **kwargs):

        if str(request.user.companymember.company.id) == self.kwargs["pk"]:

            self.success_url = reverse_lazy(
                "revenues",
                kwargs={"pk": request.user.companymember.company.id}
            )

            return super(AddRevenueView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def form_valid(self, form, *args, **kwargs):
        new_document = form.save()
        new_document.company = Company.objects.get(pk=self.kwargs["pk"])
        new_document.save()
        return super(AddRevenueView, self).form_valid(form)


class AddExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = AddExpenseForm
    success_url = ""

    def dispatch(self, request, *args, **kwargs):

        if str(request.user.companymember.company.id) == self.kwargs["pk"]:

            self.success_url = reverse_lazy(
                "expenses",
                kwargs={"pk": request.user.companymember.company.id}
            )

            return super(AddExpenseView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def form_valid(self, form, *args, **kwargs):
        new_document = form.save()
        new_document.company = Company.objects.get(pk=self.kwargs["pk"])
        new_document.save()
        return super(AddExpenseView, self).form_valid(form)


class ModifyRevenueView(LoginRequiredMixin, UpdateView):
    model = Revenue
    form_class = ModifyRevenueForm
    template_name_suffix = '_update_form'
    success_url = ""


    def dispatch(self, request, *args, **kwargs):
        document_data = Revenue.objects.get(pk=self.kwargs["pk"])

        if request.user.companymember.company.id == document_data.company.id:

            self.success_url = reverse_lazy(
                "revenues",
                kwargs={"pk": request.user.companymember.company.id}
            )

            return super(ModifyRevenueView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def form_valid(self, form, *args, **kwargs):
        new_document = form.save()
        new_document.company = Company.objects.get(pk=self.kwargs["pk"])
        new_document.save()
        return super(ModifyRevenueView, self).form_valid(form)


class ModifyExpenseView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ModifyExpenseForm
    template_name_suffix = '_update_form'
    success_url = ""


    def dispatch(self, request, *args, **kwargs):
        document_data = Expense.objects.get(pk=self.kwargs["pk"])

        if request.user.companymember.company.id == document_data.company.id:

            self.success_url = reverse_lazy(
                "expenses",
                kwargs={"pk": request.user.companymember.company.id}
            )

            return super(ModifyExpenseView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden('Forbidden.')

    def form_valid(self, form, *args, **kwargs):
        new_document = form.save()
        new_document.company = Company.objects.get(pk=self.kwargs["pk"])
        new_document.save()
        return super(ModifyExpenseView, self).form_valid(form)
