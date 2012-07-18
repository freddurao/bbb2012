#-*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from bbb2012.polls.models import Choice, Poll
from django.template import RequestContext
from django.conf import settings
from os import remove
from django.views.decorators.cache import cache_page

def main_index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response("polls/main-index.html",{'latest_poll_list': latest_poll_list}, RequestContext(request))

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list},RequestContext(request))

@cache_page(60 * 15)
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    param  = {'poll': p}
    param.update(captcha(request))
    return render_to_response('polls/detail.html',param,RequestContext(request))

@cache_page(60 * 15)
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    dist_captcha = captcha(request)

    if dist_captcha.has_key('error'):
        param  = {'poll': p,'error_message': "Captcha Incorreto."}
        param.update(dist_captcha)        
        return render_to_response('polls/detail.html',param,RequestContext(request))
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        param  =  {'poll': p,'error_message': "Voce precisa votar!.",}
        param.update(dist_captcha)            
        return render_to_response('polls/detail.html',param,RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        update_choice_percentual(p)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.


        return HttpResponseRedirect(reverse('polls.views.results_same_screen',args=(p.id,)))

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
    param  = {'poll': p}
    param.update(captcha(request))
    return render_to_response('polls/detail.html',param,RequestContext(request))

def captcha(request):
        # random generator
        from random import choice
        # PIL elements, sha for hash
        import Image, ImageDraw, ImageFont, sha
        # create a 5 char random strin and sha hash it, note that there is no big i
        SALT = settings.SECRET_KEY[:20]
        imgtext = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
        # create hash
        imghash = sha.new(SALT+imgtext).hexdigest()
        # create an image with the string (media is the folder with static files accessed by /site_media)
        # PIL "code" - open image, add text using font, save as new
        im=Image.open('static/img/bg.jpg')
        draw=ImageDraw.Draw(im)
        font=ImageFont.truetype('static/img/SHERWOOD.TTF', 18)
        draw.text((10,10),imgtext, font=font, fill=(20,20,20))
        # save as a temporary image
        # I use user IP for the filename, SITE_IMAGES_DIR_PATH - system path to folder for images
        #temp = settings.MEDIA_URL+ 'img/    ' + request.META['REMOTE_ADDR'] + '.jpg'
        temp = 'static/img/temp_image.jpg'
        #tempname = request.META['REMOTE_ADDR'] + '.jpg'
        tempname = 'temp_image.jpg'
        im.save(temp, "JPEG")
        
        if request.POST:
            data = request.POST.copy()
            # does the captcha math ?
            if data['imghash'] == sha.new(SALT+data['imgtext']).hexdigest():
                # captcha ok
                # save data etc.
                # use another view/template in render_to_response and delete the temp captcha file:
                #remove(temp)
                #return render_to_response('polls/detail.html', {'ok': True, 'hash': imghash, 'tempname': tempname},RequestContext(request))
                return {'ok': True, 'hash': imghash, 'tempname': tempname}
            else:
                # captcha bad
                # return the form
                #return render_to_response('polls/detail.html', {'error': True, 'hash': imghash, 'tempname': tempname},RequestContext(request))
                return {'error': True, 'hash': imghash, 'tempname': tempname}
        # no post data, show the form
        else:
            #return render_to_response('polls/detail.html', {'hash': imghash, 'tempname': tempname},RequestContext(request))    
            return {'hash': imghash, 'tempname': tempname}    