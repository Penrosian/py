import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text="question", days=0, choices=[]):
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    for choice_text in choices:
        question.choice_set.create(choice_text=choice_text, votes=0)
    return question

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self):
        past_question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question],
        )

    def test_two_past_questions(self):
        past_question1 = create_question(question_text="Past question 1.", days=-30)
        past_question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question2, past_question1],
        )

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        question = create_question(question_text="Future question.", days=30)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_question = create_question(question_text="Old question.", days=-30)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_question = create_question(question_text="Recent question.", days=-0.5)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        response = self.client.get(reverse("polls:detail", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past Question.", days=-5)
        response = self.client.get(reverse("polls:detail", args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)

class QuestionVotingTests(TestCase):
    def test_vote_on_future_question(self):
        future_question = create_question(question_text="Future question.", days=5, choices=["Choice 1", "Choice 2"])
        response = self.client.post(reverse("polls:vote", args=(future_question.id,)), {"choice": future_question.choice_set.first().id})
        self.assertEqual(response.status_code, 404)

    def test_vote_on_past_question_without_choice(self):
        past_question = create_question(question_text="Past Question.", days=-5, choices=["Choice 1", "Choice 2"])
        response = self.client.post(reverse("polls:vote", args=(past_question.id,)), {})
        self.assertContains(response, "You didn&#x27;t select a choice.")

    def test_vote_on_past_question_with_valid_choice(self):
        past_question = create_question(question_text="Past Question.", days=-5, choices=["Choice 1", "Choice 2"])
        response = self.client.post(reverse("polls:vote", args=(past_question.id,)), {"choice": past_question.choice_set.first().id})
        self.assertRedirects(response, reverse("polls:results", args=(past_question.id,)))
        past_question.choice_set.first().refresh_from_db()
        self.assertEqual(past_question.choice_set.first().votes, 1)

class FailingTests(TestCase):
    def test_fail_example(self):
        self.assertEqual(1, 2)