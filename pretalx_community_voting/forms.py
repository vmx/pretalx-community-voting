from django import forms


class SignupForm(forms.Form):
    email = forms.EmailField(required=True)

    def send_email(self):
        """Send the email once the form was validated."""
        print(f'sending the email to {self.cleaned_data["email"]}')
