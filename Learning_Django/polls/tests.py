from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

import datetime

# Create your tests here.

def create_question(question_text, days):
    """
    This creates an object of the question model
    The question pub_date is timezone.now() + days, with future day positive and past days negative
    """
    

    date = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(question_text = question_text, pub_date=date)    

class QuestionModelsTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_recently_published() returns false for questions with future pub_date"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False) 


    def test_was_published_recently_with_old_question(self):
        """was_recently_published() returns false for questions with old pub_date ie older than 1 day """
        
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)

        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False) 


    def test_was_published_recently_with_recent_question(self):
        """was_recently_published() returns true for questions with recent pub_date ie within 1 day """
        
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=50)

        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True) 



class QuestionIndexViewTest(TestCase):

    def test_with_no_question(self):
        """This tests if no question is displayed on the index page when there is no questions"""

        url = reverse("polls:index")
        response = self.client.get(url)

        self.assertIs(response.status_code, 200)
        self.assertContains(response, "No poll to available. Come back later.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    
    def test_with_future_question(self):
        """This tests if no question is displayed on the index page when there is only future questions"""

        future_question = create_question("", 1)

        url = reverse("polls:index")
        response = self.client.get(url)

        self.assertIs(response.status_code, 200)
        self.assertContains(response, "No poll to available. Come back later.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_with_past_question(self):
        """This tests if question is displayed on the index page when there is past questions"""

        past_question = create_question("Past question", -1)

        url = reverse("polls:index")
        response = self.client.get(url)

        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])


    def test_with_past_and_future_questions(self):
        """This tests if question is displayed on the index page when there are past and future questions"""

        past_question = create_question("Past Question", -1)
        future_question = create_question("Future Question", 1)

        url = reverse("polls:index")
        response = self.client.get(url)

        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])


    def test_with_multiple_past_questions(self):
        """This tests if questions are displayed on the index page when there are multiple past questions"""

        past_question0 = create_question("Past question0", -1)
        past_question1 = create_question("Past question1", -2)
        past_question2 = create_question("Past question2", -4)
        past_question3 = create_question("Past question3", -6)

        url = reverse("polls:index")
        response = self.client.get(url)

        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question0, past_question1, past_question2, past_question3])



class QuestionDetialViewTest(TestCase):

    def test_with_past_question(self):
        """Test the view page with a past question"""

        past_question = create_question("Past Question", -1)

        url = reverse("polls:detail", args=(past_question.id,))
        print(url, " this is the url")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["question"], past_question)


    def test_with_future_question(self):
        """Test the view page with a future question"""

        future_question = create_question("future Question", 1)

        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class QuestionResultsView(TestCase):

    def test_with_past_question(self):
        """
        This is to test result page for past question
        """

        past_question = create_question("Past_question", -1)

        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["question"], past_question)


    def test_with_future_question(self):
        """
        This is to test result page for future question
        """

        future_question = create_question("Future Question", 1)

        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)



# class voteViewTest(TestCase):
#     """
#     tests the vote view
#     """

#     def test_with_no_choice_choosen(self):
#         """
#         tests if vote view renders detail template with the error argument
#         """

#         question = create_question("Question", 0)

#         url = reverse("polls:vote", args=(question.id,))
#         response = self.client.get(url)

        # self.assertEqual(response.status_code, 404)
        # self.assertContains(response, "You didn't vote.")
