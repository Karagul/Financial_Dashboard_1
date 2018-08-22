from dashapp.forms import LoginForm, RegisterForm

def global_login_form(request):
    return {"global_login_form": LoginForm}

def global_register_form(request):
    return {"global_register_form": RegisterForm}