from django.forms import ModelForm, CharField, TextInput
from .models import Swits


class SwitForm(ModelForm):

    text = CharField(min_length=5, widget=TextInput())

    class Meta:
        model = Swits
        fields = ['text']
        exclude = ['likes']