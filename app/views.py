from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from app.models import *


def paginate(objects_list, request, limit=3):
    paginator = Paginator(objects_list, limit)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def index(request):
    content = paginate(Question.objects.all(), request)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'index.html', {'questions': content, 'popular_tags': popular_tags})


def ask(request):
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'ask.html', {'popular_tags': popular_tags})


def question(request, pk):
    main_question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.by_question(pk), request, limit=3)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'one_question_page.html', {'main_question': main_question, 'answers': answers_page,
                                                      'popular_tags': popular_tags})


def hot(request):
    content = paginate(Question.objects.hot(), request)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'index.html', {'questions': content, 'popular_tags': popular_tags})


def tag(request, tag):
    questions_page = paginate(Question.objects.by_tag(tag), request)
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'question_by_tag.html', {'questions': questions_page, 'tag': tag,
                                                    'popular_tags': popular_tags})


def settings(request):
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'settings.html', {"popular_tags": popular_tags})


def login(request):
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'login.html', {'popular_tags': popular_tags})


def signup(request):
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'signup.html', {'popular_tags': popular_tags})
