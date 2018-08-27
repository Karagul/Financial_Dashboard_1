from dashapp.forms import LoginForm


def global_login_form(request):
    return {"global_login_form": LoginForm}
