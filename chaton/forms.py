import hashlib

from django import forms

from chaton import models


class MessageForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = models.Message
        fields = ['message']


class MessageRespondForm(forms.ModelForm):

    class Meta:
        model = models.Message
        fields = ['message']


class ChatForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text='can be empty')

    def save(self, commit=True):
        obj = super(ChatForm, self).save(commit=False)
        obj.password_hash = hashlib.md5(self.cleaned_data['password'].encode('utf-8')).hexdigest()
        if commit:
            obj.save()
        return obj

    class Meta:
        model = models.Chat
        fields = ['title']


class ChatLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)