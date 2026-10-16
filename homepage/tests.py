"""Тесты главной страницы и обработчика 404 (ПР5)."""

from django.test import SimpleTestCase


class HomepageTests(SimpleTestCase):
    def test_index_opens(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "InquiryDesk")
        self.assertContains(response, "bootstrap@5.3.3")

    def test_index_has_navigation(self):
        response = self.client.get("/")
        self.assertContains(response, 'href="/inquiries/"')
        self.assertContains(response, 'href="/categories/"')

    def test_unknown_url_uses_custom_404(self):
        # При запуске тестов Django работает с DEBUG = False,
        # поэтому срабатывает собственный обработчик handler404.
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response, "404 – страница не найдена", status_code=404,
        )
