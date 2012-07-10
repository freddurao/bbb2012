from django.db.models.signals import post_save
from django.db import models
from PIL import Image
import datetime

'''
It creates the questions poll and the publicatioon date of the poll.
'''
class Poll(models.Model):

    question = models.CharField(max_length=200)

    pub_date = models.DateTimeField('Publication Date')

    def __unicode__(self):
        return self.question

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()

    was_published_today.short_description = 'Publishing Today?'

'''
It creates alternatives for a previously created poll.
'''
class Choice(models.Model):
    
    poll = models.ForeignKey(Poll)
    
    candidate = models.CharField(max_length=200)

    candidate_photo = models.ImageField(upload_to="static/img/")    
    
    votes = models.IntegerField(default=0)

    percentual = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.candidate