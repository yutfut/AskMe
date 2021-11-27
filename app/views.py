from django.shortcuts import render
from django.core.paginator import Paginator

def index(request):
    questions = [
        {
            'title': f'title {i}',
            'text': f'text {i}',
        } for i in range(1000)
    ]
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'index.html', context)


def hot(request):
    questions = [
        {
            'title': f'title {i}',
            'text': f'text {i}',
        } for i in range(10)
    ]
    paginator = Paginator(questions, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'hot.html', context)


def ask(request):
    return render(request, 'ask.html')


def question(request):
    answers = [
        {
            'text': f'text {i}',
        } for i in range(10)
    ]
    context = {'answers': answers}
    return render(request, 'question.html', context)


def tag(request):
    return render(request, 'tag.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
