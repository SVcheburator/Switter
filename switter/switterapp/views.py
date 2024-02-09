from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .forms import SwitForm, CommentForm
from .models import Swits, Likes, Dislikes, Comments


# Main
def main(request):
    swits = Swits.objects.all()

    for swit in swits:
        swit.likes = Likes.objects.filter(swit_id=swit.id).count()
        swit.dislikes = Dislikes.objects.filter(swit_id=swit.id).count()

    return render(request, 'switterapp/index.html', {'swits': swits})


# Swits
@login_required
def add_swit(request):
    if request.method == 'POST':
        form = SwitForm(request.POST, request.FILES)
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


# Reactions
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

    return redirect(to='switterapp:detail_swit', swit_id=swit_id)


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

    return redirect(to='switterapp:detail_swit', swit_id=swit_id)


# Comments
@login_required(login_url='/users/login/')
def add_comment(request, swit_id):
    swit = get_object_or_404(Swits, pk=swit_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():                                                                 
            new_comment = form.save(commit=False)
            new_comment.swit = swit
            new_comment.user = request.user
            new_comment.save()
            return redirect(to='switterapp:show_comments', swit_id=swit_id)
        else:
            return render(request, 'switterapp/add_comment.html', {'swit_id': swit_id, 'form': form})
    
    return render(request, 'switterapp/add_comment.html', {'swit_id': swit_id, 'form': CommentForm})


def show_comments(request, swit_id):
    comments = Comments.objects.filter(swit_id=swit_id)
    return render(request, 'switterapp/show_comments.html', {'swit_id': swit_id, 'comments': comments})