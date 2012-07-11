#-*- coding: utf-8 -*-
from datetime import datetime

from django.test import TestCase
from django.test import Client

from bbb2012.polls.models import Poll, Choice

class PollTest(TestCase):
    
    def setUp(self):
        question="Quem será eliminado do BBB 2012"
        now = datetime.now()
        self.poll = Poll.objects.create(question=question, pub_date=now)
        self.poll.choice_set.create(candidate="Fred",votes=0,percentual=0.0,candidate_photo="fred.png")
        self.poll.choice_set.create(candidate="Marcel",votes=0,percentual=0.0,candidate_photo="marcel.png")

    def test_dos_modelos(self):
        
        self.assertEqual(self.poll.choice_set.all().count(), 2)
        self.assertNotEqual(self.poll.choice_set.all().count(), 0)

    def test_same_candidate(self):
        self.assertNotEqual(self.poll.choice_set.all()[0].candidate, self.poll.choice_set.all()[1].candidate)

    def test_de_voto(self):
        c = Client()
        # Fazendo o primeiro voto
        response = c.post('/polls/1/vote/', {'choice': '1',})
        # Verficicando se nao ha votos
        self.assertEqual(response.status_code, 302)
        # Verificando se ha um voto
        choice = Choice.objects.get(pk=1)
        self.assertEqual(choice.votes, 1)