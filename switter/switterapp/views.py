from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .forms import SwitForm
from .models import Swits, Likes, Dislikes

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
    likes = Likes.objects.filter(swit_id=swit_id).count()
    dislikes = Dislikes.objects.filter(swit_id=swit_id).count()
    return render(request, 'switterapp/detail_swit.html', {'swit': swit, 'likes': likes, 'dislikes': dislikes})



@login_required(login_url='/users/login/')
def like_swit(request, swit_id):
    swit = get_object_or_404(Swits, pk=swit_id)
    user = request.user
    try:
        Likes.objects.create(user=user, swit=swit)
        try:
            Dislikes.objects.get(swit_id=swit_id, user_id=user.id).delete()
        except ObjectDoesNotExist:
            ...
    except IntegrityError:
        Likes.objects.get(swit_id=swit_id, user_id=user.id).delete()

    likes = Likes.objects.filter(swit_id=swit_id).count()
    dislikes = Dislikes.objects.filter(swit_id=swit_id).count()

    return render(request, 'switterapp/detail_swit.html', {'swit': swit, 'likes': likes, 'dislikes': dislikes})


@login_required(login_url='/users/login/')
def dislike_swit(request, swit_id):
    swit = get_object_or_404(Swits, pk=swit_id)
    user = request.user
    try:
        Dislikes.objects.create(user=user, swit=swit)
        try:
            Likes.objects.get(swit_id=swit_id, user_id=user.id).delete()
        except ObjectDoesNotExist:
            ...
    except IntegrityError:
        Dislikes.objects.get(swit_id=swit_id, user_id=user.id).delete()

    likes = Likes.objects.filter(swit_id=swit_id).count()
    dislikes = Dislikes.objects.filter(swit_id=swit_id).count()
    
    return render(request, 'switterapp/detail_swit.html', {'swit': swit, 'likes': likes, 'dislikes': dislikes})
