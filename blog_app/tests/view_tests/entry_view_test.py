from blog_app.factories.entry_factory import EntryFactory
from blog_app.models.entry import Entry
from cryptek.qa_templates import ClassBaseViewTestCase


class EntryViewTestCase(ClassBaseViewTestCase):
    endpoint_name = "blog_app:entry_detail"
    is_authenticated = True

    def setUp(self):
        entry = EntryFactory.create(status=1)
        self.kwargs = {"slug": entry.slug}
        super().setUp()

    def test_get(self):
        response = self.get()
        self.response_code(response=response, status_code=200)
        self.assertTemplateUsed(response, "entry_detail.html")

    def test_get_correct_content(self):
        response = self.get()
        self.response_code(response=response, status_code=200)

    def test_get_no_content(self):
        Entry.objects.all().delete()
        response = self.get()
        self.response_code(response=response, status_code=404)

    def test_incorrect_slug(self):
        self.kwargs = {"slug": "incorrect-slug"}
        response = self.get()
        self.response_code(response=response, status_code=404)

    def test_get_login(self):
        with self.login():
            response = self.get()
            self.response_code(response=response, status_code=200)
            self.assertTemplateUsed(response, "entry_detail.html")

    def test_get_logout(self):
        with self.logout():
            response = self.get()
            self.response_code(response=response, status_code=200)
            self.assertTemplateUsed(response, "entry_detail.html")

    def test_unicode_slug(self):
        """Test that a slug with non-ASCII characters works."""
        entry = EntryFactory.create(status=1, title="Título con caracteres especiales")
        self.kwargs = {"slug": entry.slug}
        response = self.get()
        self.response_code(response=response, status_code=200)
        self.assertTemplateUsed(response, "entry_detail.html")
