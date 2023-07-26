# Create your views here.
# import datetime
import sys

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import RemainderForm
from .tasks import send_postponed_email


def send_email(request):
    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form and populate it with data:
        form = RemainderForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            reminder_text = form.cleaned_data['reminder_text']
            reminder_datetime = form.cleaned_data['reminder_datetime']

            send_postponed_email.apply_async(
                kwargs={"subject": "Reminder",
                        "message": reminder_text,
                        "from_email": settings.NO_REPLY_EMAIL,
                        "recipient_list": [email, ],
                        },
                eta=reminder_datetime
            )

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('success'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_reminder_datetime = timezone.now() + timezone.timedelta(days=1)
        form = RemainderForm(initial={'reminder_datetime': proposed_reminder_datetime, })

    return render(request, 'send_email.html', {'form': form})


def success(request):
    return render(request, 'success.html')
