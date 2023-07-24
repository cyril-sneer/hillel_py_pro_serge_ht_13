# Create your views here.
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RemainderForm


def index(request):
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

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('success'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_reminder_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
        form = RemainderForm(initial={'reminder_datetime': proposed_reminder_datetime, })

    return render(request, 'index.html', {'form': form})


def success(request):
    return render(request, 'success.html')
