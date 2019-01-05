from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Question


# Create your tests here.


def create_question(question_text, days):
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# class QuestionModelTest(TestCase):
#
#     def test_was_published_recently_with_future_question(self):
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)
#
#     def test_was_published_recently_with_old_question(self):
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_question = Question(pub_date=time)
#         self.assertIs(old_question.was_published_recently(), False)
#
#     def test_was_published_recently_with_old_question(self):
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No blog are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="past question", days=-30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: past question>'])

    def test_future_question(self):
        create_question(question_text="future question", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "No blog is available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="past question", days=-30)
        create_question(question_text="future question", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="past question 1", days=-30)
        create_question(question_text="past question 2", days=-5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question 2>', '<Question: past question 1>']
        )

#
# class QuestionDetailViewTest(TestCase):
#     def test_future_question(self):
#         future_question = create_question(question_text='future question', days=5)
#         url = reverse('blog:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_question(self):
#         past_question = create_question(question_text='past_question', days=-5)
#         url = reverse('blog:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)
