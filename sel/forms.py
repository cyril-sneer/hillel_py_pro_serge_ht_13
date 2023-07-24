import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class RemainderForm(forms.Form):
    email = forms.EmailField(label='Input e-mail')
    reminder_text = forms.CharField(label='Reminder text', widget=forms.Textarea)
    reminder_datetime = forms.DateTimeField(label='Reminder date & time')

    def clean_reminder_datetime(self):
        data = self.cleaned_data['reminder_datetime']

        if data < timezone.now():
            raise ValidationError('Invalid value - time in the past!')

        if data > timezone.now() + datetime.timedelta(days=2):
            raise ValidationError('Invalid value - time more than 2 days ahead!')

        return data


