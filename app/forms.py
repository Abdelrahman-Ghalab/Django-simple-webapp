from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

class AddVacation(forms.Form):
    start_date = forms.DateField(
        required= True,
        label = 'start_date'
    )
    end_date = forms.DateField(
        required= True,
        label= 'end_date',
    )

    description = forms.CharField(
        required=  True,
        label = "description",
        max_length = 500,
    )


class UserLoginForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length= 32
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )