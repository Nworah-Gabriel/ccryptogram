from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70)
    password= forms.CharField(widget=forms.PasswordInput)

class SignupFormextra(forms.Form):
    wallet_address = forms.CharField(max_length=70)
    moblie_number = forms.CharField(max_length=70)
    occupation = forms.CharField(max_length=70)
    alternate_email = forms.EmailField()
    date_of_birth = forms.DateField()
    country = forms.CharField(max_length=70)
    


class SignupForm(forms.Form):
    username = forms.CharField(max_length=70)
    password= forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    firstname = forms.CharField(max_length=70)
    lastname = forms.CharField(max_length=70)


class ContactUsForm(forms.Form):
    message = forms.CharField(max_length=2000)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=70)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField( max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!')

class SubscriberForm(forms.Form):
     email = forms.EmailField()

class UserMessageForm(forms.Form):
    """
    A class based form for capturing the users transaction requests
    """

    message = forms.CharField(max_length=5000)
    Transaction_Amount = forms.CharField(max_length=500)
    wallet_address = forms.CharField(max_length=500)
