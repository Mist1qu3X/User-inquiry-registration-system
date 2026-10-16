"""Тесты страниц категорий (ПР5)."""

from django.test import SimpleTestCase

import storage


class CategoryPagesTests(SimpleTestCase):
    def test_list_shows_categories_from_json(self):
        _, categories, _, _ = storage.load_all()
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)
        for category in categories:
            self.assertContains(response, category.name)

    def test_detail_existing_category(self):
        _, categories, _, _ = storage.load_all()
        category = categories[0]
        response = self.client.get(f"/categories/{category.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, category.name)

    def test_detail_missing_category_returns_404(self):
        response = self.client.get("/categories/999/")
        self.assertContains(
            response, "Категория не найдена", status_code=404,
        )
