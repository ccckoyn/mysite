from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from django.views import generic

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {'latest_question_list':latest_question_list}
    # return render(request, 'polls/index.html', context)
    # output = ','.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # return HttpResponse("Hello, Django. You're at the polls index.")

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    '''
    方法一
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    '''
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question':question})
    '''
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
    '''

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    # return HttpResponse("You're voting on question %s." % question_id)

# Create your views here.
