from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def ask(request):
    return render(request, 'ask.html')


def question(request):
    return render(request, 'question.html')


def tag(request):
    return render(request, 'tag.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
