from django.shortcuts import render

from .models import TodayMass
from django.views import generic

class NewMass(generic.CreateView):
    pass


class AddToMass(generic.UpdateView):
    pass

class ViewMass(generic.DetailView):
    pass
