from django.test import TestCase, Client
from accounts.models import Student

# Create your tests here.
class TestAccount(TestCase):
    
    def setUp(self):
        stu = Student(
            first_name = 'mohcine',
            last_name = 'sahtani',
            username = 'mohcine_sahtani',
            email = 'mohcine.sahtani@gmail.com',
        )
        stu.set_password('mohcines2001')
        stu.save()

    def test_login(self):
        cli = Client()
        res = cli.login(username="mohcine_sahtani", password="mohcines2001")
        self.assertTrue(res)
