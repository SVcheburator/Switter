from django.forms import ModelForm, CharField, TextInput
from .models import Swits, Comments


class SwitForm(ModelForm):

    text = CharField(min_length=5, widget=TextInput())

    class Meta:
        model = Swits
        fields = ['text', 'image']
        exclude = ['likes']


class CommentForm(ModelForm):

    text = CharField(min_length=5, widget=TextInput())

    class Meta:
        model = Comments
        fields = ['text']