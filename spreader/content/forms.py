from django import forms
from django.core.validators import URLValidator, MaxLengthValidator

url_validator = URLValidator()
class SubmitImage(forms.Form):
    url = forms.CharField(validators=[url_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. http://i.imgur.com/iIfEEn6.jpg'}), max_length=300)
    caption = forms.CharField(validators=[MaxLengthValidator(1000)], widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Caption.'}), max_length=1000, required=False)

class SubmitComment(forms.Form):
    comment = forms.CharField(validators=[MaxLengthValidator(300)], widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}), max_length=300)
