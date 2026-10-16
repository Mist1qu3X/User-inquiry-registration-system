"""Тесты страниц обращений (ПР5)."""

from django.test import SimpleTestCase

import storage


class InquiryPagesTests(SimpleTestCase):
    def test_list_shows_inquiries_from_json(self):
        _, _, _, inquiries = storage.load_all()
        response = self.client.get("/inquiries/")
        self.assertEqual(response.status_code, 200)
        for inquiry in inquiries:
            self.assertContains(response, f'href="/inquiries/{inquiry.id}/"')

    def test_detail_existing_inquiry(self):
        _, _, _, inquiries = storage.load_all()
        inquiry = inquiries[0]
        response = self.client.get(f"/inquiries/{inquiry.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, inquiry.status.title)
        self.assertContains(response, inquiry.author.name)

    def test_detail_missing_inquiry_returns_404(self):
        response = self.client.get("/inquiries/999/")
        self.assertContains(
            response, "Обращение не найдено", status_code=404,
        )

    def test_int_converter_rejects_text(self):
        response = self.client.get("/inquiries/abc/")
        self.assertEqual(response.status_code, 404)
