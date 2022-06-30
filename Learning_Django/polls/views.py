from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader 
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # return Question.objects.order_by("-pub_date")[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

def index(request):
    latest_question_list = Question.objects.order_by("pub_date")[:5]
    response = "/n".join(question.question_text for question in latest_question_list)

    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list" : latest_question_list,
    }


    # html_response = ""

    # for question in latest_question_list:
        # html_question_div = "<div>"
        # html_question_h3 = f"<h3>{question.question_text}</h3>"

        # html_choice_list = "<ul>"

        # for choice in question.choice_set.all():
        #     choice_li = f"<li>{choice.choice_text}</li>"
        #     html_choice_list = html_choice_list + choice_li 
        
        # html_choice_list = html_choice_list + "</ul>"
        
        # html_question_div = html_question_div + html_question_h3 + html_choice_list
        # html_question_div = html_question_div + "</div>"

        # html_response = html_response + html_question_div

    # return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html" , context)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    


def detail(request, question_id):

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question Doesn't Exist.")

    question = get_object_or_404(Question, pk=question_id)

    context = {
        "question" : question,
    }

    # return HttpResponse(f"You're looking at question {question_id}.")
    return render(request, "polls/detail.html" , context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    


def results(request, question_id):
    # response = f"You're looking at the results of question {question_id}."
    # return HttpResponse(response)

    question = get_object_or_404(Question, pk=question_id)

    context = {
        "question" : question,
    }
    return render(request, "polls/results.html", context) 


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        seleted_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        error_message = "You didn't vote."
        context = {
            "question" : question,
            "error_message" : error_message,
        }
        return render(request, "/polls/detail.html", context)

        # return HttpResponseRedirect(reverse("polls:detail", args=(question_id,)), context)

    seleted_choice.votes += 1
    seleted_choice.save()

    # return HttpResponse(f"You're voting on question {question_id}.")

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))