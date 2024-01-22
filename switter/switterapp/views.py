from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import SwitForm
from .models import Swits

# Create your views here.
def main(request):
    swits = Swits.objects.all()
    return render(request, 'switterapp/index.html', {'swits': swits})


@login_required
def add_swit(request):
    if request.method == 'POST':
        form = SwitForm(request.POST)
        if form.is_valid():
            new_swit = form.save(commit=False)
            new_swit.user = request.user
            new_swit.save()
            return redirect(to='switterapp:main')
        else:
            return render(request, 'switterapp/add_swit.html', {'form': form})

    return render(request, 'switterapp/add_swit.html', {'form': SwitForm})


def detail_swit(request, swit_id):
    swit = get_object_or_404(Swits, pk=swit_id)
    return render(request, 'switterapp/detail_swit.html', {"swit": swit})
