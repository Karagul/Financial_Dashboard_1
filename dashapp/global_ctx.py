from dashapp.forms import LoginForm, CompanyRegisterForm, UserRegisterForm


def global_login_form(request):
    return {"global_login_form": LoginForm}
