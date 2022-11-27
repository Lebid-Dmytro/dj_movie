from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, RettingStar, Rating


class ReviewForm(forms.ModelForm):
    '''Форми відгуків'''
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'test', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control border"}),
            'email': forms.EmailInput(attrs={"class": "form-control border"}),
            'text': forms.Textarea(attrs={"class": "form-control border"})
        }


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RettingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)

