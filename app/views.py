from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth

from django.contrib.auth.decorators import login_required

from app.models import *
from app.forms import *


def paginate(objects_list, request, limit=10):
    paginator = Paginator(objects_list, limit)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def index(request):
    page = paginate(Question.objects.all(), request)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'index.html', {'page': page, 'popular_tags': popular_tags})


def ask(request):
    if request.user.is_authenticated:
        popular_tags = Tag.objects.popular_tags()
        if request.method == 'GET':
            form = AskForm()
        elif request.method == 'POST':
            form = AskForm(request.user.profile, data=request.POST)
            if form.is_valid():
                post = form.save()
                # return redirect(reverse('index'))
                return redirect(reverse('question', kwargs={'pk': post.pk}))
        return render(request, 'ask.html', {
            'form': form,
            'popular_tags': popular_tags,
        })
    else:
        return redirect(reverse('login'))


def question(request, pk):
    question = Question.objects.get(id=pk)
    page = paginate(Answer.objects.by_question(pk), request, limit=5)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'question.html', {'question': question, 'page': page,
                                                      'popular_tags': popular_tags})


def hot(request):
    page = paginate(Question.objects.hot(), request)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'hot.html', {'page': page, 'popular_tags': popular_tags})


def tag(request, tag):
    page = paginate(Question.objects.by_tag(tag), request)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'tag.html', {'page': page,
                                        'tag': tag,
                                        'popular_tags': popular_tags})


@login_required
def settings(request):
    form_updated = False
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 'email': request.user.email})
        ava = ImageForm()
    else:
        form = SettingsForm(user=request.user, data=request.POST)
        ava = ImageForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid() and ava.is_valid():
            user = form.save()
            ava.save()
            form_updated = True
            login(request, user)
    popular_tags = Tag.objects.popular_tags()
    return render(request, 'settings.html', {
        'form': form,
        'form_updated': form_updated,
        'ava': ava,
        'popular_tags': popular_tags,
    })


def login(request):
    popular_tags = Tag.objects.popular_tags()
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, 'User not found')
            else:
                auth.login(request, user)
                return redirect(request.POST.get('next', '/'))
    return render(request, 'login.html', {'form': form,
                                          'popular_tags': popular_tags})


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(request.POST.get('next', '/'))
    popular_tags = Tag.objects.popular_tags()
    return render(request, 'signup.html', {
        'form': form,
        'popular_tags': popular_tags,
    })


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))
