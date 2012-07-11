#-*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from bbb2012.polls.models import Choice, Poll
from django.template import RequestContext

def main_index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response("polls/main-index.html",{'latest_poll_list': latest_poll_list}, RequestContext(request))


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]

    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list},RequestContext(request))


def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},RequestContext(request))

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "Voce precisa votar!.",
        },RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        update_choice_percentual(p)
        
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls.views.results_same_screen', args=(p.id,)))

def update_choice_percentual(p):
    total_votes = 0

    total_votes = sum([choice.votes for choice in p.choice_set.all()])
 
    for choice in p.choice_set.all():
        choice.percentual = round(choice.votes / total_votes,2) * 100
        choice.save()
        

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p},RequestContext(request))

def results_same_screen(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},RequestContext(request))