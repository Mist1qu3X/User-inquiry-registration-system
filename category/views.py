"""View-функции приложения category: список и страница категории (ПР5).

Используются функции ПР3 из categories.py и inquiries.py; список обращений
категории формируется общей функцией inquiry_items() приложения inquiry.
"""

from django.http import HttpResponse
from django.utils.html import escape

import categories as categories_module
import inquiries as inquiries_module
import storage
from homepage.views import page
from inquiry.views import inquiry_items


def availability_badge(category):
    """Бейдж доступности категории для регистрации новых обращений."""
    if category.is_available():
        return '<span class="badge text-bg-success">открыта</span>'
    return '<span class="badge text-bg-secondary">закрыта</span>'


def category_list(request):
    _, categories, _, inquiries = storage.load_all()

    rows = ""
    for category in categories_module.sort_categories(categories):
        count = len(inquiries_module.filter_inquiries_by_category(
            inquiries, category.id,
        ))
        rows += f"""
        <tr>
            <td>
                <a href="/categories/{category.id}/">
                    {escape(category.name)}
                </a>
            </td>
            <td>{availability_badge(category)}</td>
            <td class="text-end">{count}</td>
        </tr>"""

    content = f"""
    <h1 class="mb-3">Категории</h1>
    <div class="table-responsive">
        <table class="table table-hover bg-white border">
            <thead>
                <tr>
                    <th>Категория</th>
                    <th>Приём обращений</th>
                    <th class="text-end">Обращений</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
    return HttpResponse(page("InquiryDesk – категории", content))


def category_detail(request, category_id):
    _, categories, _, inquiries = storage.load_all()
    category = categories_module.find_category(categories, category_id)

    if category is None:
        content = """
        <h1 class="text-danger">Категория не найдена</h1>
        <a href="/categories/" class="btn btn-outline-secondary">
            ← к списку категорий
        </a>
        """
        return HttpResponse(
            page("Категория не найдена", content),
            status=404,
        )

    selected = inquiries_module.filter_inquiries_by_category(
        inquiries, category.id,
    )
    content = f"""
    <h1 class="mb-2">{escape(category.name)}</h1>
    <p>{availability_badge(category)}
        <span class="ms-2 text-body-secondary">
            обращений в категории: {len(selected)}
        </span>
    </p>
    {inquiry_items(selected)}
    <a href="/categories/" class="btn btn-outline-secondary mt-3">
        ← к списку категорий
    </a>
    """
    return HttpResponse(page(category.name, content), status=200)
