from django.contrib.auth import get_user_model, forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class NewUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["username"].label = "Display Name"
            self.fields["email"].label = "Email Address"


class ChangeUserInfoForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")
