from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from dashapp.forms import TestForm1


class HomePageView(TemplateView):
    template_name = "home.html"


class TestTableView(TemplateView):
    template_name = "table.html"


class TestFormView(FormView):
    template_name = "form.html"
    form_class = TestForm1
