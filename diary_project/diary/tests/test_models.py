from django.test import TestCase
from django.contrib.auth import get_user_model
from diary.models import Entry, Tag

User = get_user_model()

class EntryCaseTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username="Vadim")

    def test_case_delete(self):
        Entry.objects.create(
            author=self.author,
            title="test header",
            content="Here is the content for Django tests"
            )
        self.author.delete()
        self.assertEqual(Entry.objects.count(), 0)

    def test_case_many_to_many(self):
        entry = Entry.objects.create(
            author=self.author,
            title="test header",
            content="Here is the content for Django tests")
        tag = Tag.objects.create(name="Developers")
        entry.tags.add(tag)
        self.assertEqual(entry.tags.count(), 1)
        self.assertIn(entry, tag.entries.all())
        