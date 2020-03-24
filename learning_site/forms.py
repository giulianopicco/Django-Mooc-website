from django import forms
from django.core import validators


def must_be_empty(value):
    if value:
        raise forms.ValidationError('It is not empty')


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(help_text="Please verify your email address")
    verify_email = forms.EmailField(help_text="Please verify your email address")
    suggestion = forms.CharField(widget=forms.Textarea)
    honey_pot = forms.CharField(required=False,
                                widget=forms.HiddenInput,
                                label="Leave empty",
                                # validators=[validators.MaxLengthValidator(0)])
                                validators=[must_be_empty])

    def clean(self):
        form = self.cleaned_data
        if not form['email'] == form['verify_email']:
            raise forms.ValidationError('Yout emails does not match')

    # def clean_honey_pot(self):
    #     honey_pot = self.cleaned_data['honey_pot']
    #     if len(honey_pot):
    #         raise forms.ValidationError('this should be empyt')
    #     return honey_pot
