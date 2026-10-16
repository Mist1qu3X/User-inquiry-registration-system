"""Главная страница InquiryDesk и общий HTML-каркас всех страниц (ПР5).

Функция page() размещена в приложении homepage, потому что главная страница
задаёт общий вид остальных страниц. Приложения inquiry и category
импортируют её.
"""

from django.http import HttpResponse
from django.utils.html import escape

import inquiries as inquiries_module
import statuses as statuses_module
import storage

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)

# Цвет бейджа Bootstrap для каждого кода статуса обращения.
STATUS_BADGES = {
    "new": "text-bg-primary",
    "in_progress": "text-bg-warning",
    "resolved": "text-bg-success",
    "closed": "text-bg-secondary",
    "rejected": "text-bg-danger",
}


def page(title, content):
    """Собрать HTML-документ: кодировка, заголовок, Bootstrap, навигация."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body class="bg-body-tertiary">
    <nav class="navbar navbar-expand bg-primary mb-4" data-bs-theme="dark">
        <div class="container">
            <a class="navbar-brand fw-semibold" href="/">InquiryDesk</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/inquiries/">Обращения</a>
                <a class="nav-link" href="/categories/">Категории</a>
            </div>
        </div>
    </nav>
    <main class="container pb-5">{content}</main>
</body>
</html>"""


def status_badge(status):
    """Вернуть HTML-бейдж статуса обращения (или прочерк, если его нет)."""
    if status is None:
        return '<span class="badge text-bg-light">—</span>'
    css = STATUS_BADGES.get(status.code, "text-bg-info")
    return f'<span class="badge {css}">{escape(status.title)}</span>'


def index(request):
    _, categories, statuses, inquiries = storage.load_all()

    rows = ""
    for status in statuses_module.list_statuses(statuses):
        count = len(inquiries_module.filter_inquiries_by_status(
            inquiries, status.code,
        ))
        rows += f"""
        <li class="list-group-item d-flex justify-content-between">
            {status_badge(status)}
            <span class="fw-semibold">{count}</span>
        </li>"""

    content = f"""
    <div class="p-4 mb-4 bg-white rounded-3 border">
        <h1 class="display-5">InquiryDesk</h1>
        <p class="lead">Система регистрации обращений пользователей:
            приём обращения, отнесение к категории и отслеживание
            статуса обработки.</p>
        <a href="/inquiries/" class="btn btn-primary me-2">Обращения</a>
        <a href="/categories/" class="btn btn-outline-primary">Категории</a>
    </div>
    <div class="row g-4">
        <div class="col-md-6">
            <h2 class="h5">Обращения по статусам</h2>
            <ul class="list-group">{rows}</ul>
        </div>
        <div class="col-md-6">
            <h2 class="h5">Сводка</h2>
            <ul class="list-group">
                <li class="list-group-item">
                    Всего обращений: <strong>{len(inquiries)}</strong>
                </li>
                <li class="list-group-item">
                    Категорий: <strong>{len(categories)}</strong>
                </li>
            </ul>
        </div>
    </div>
    """
    return HttpResponse(page("InquiryDesk", content))


def page_not_found(request, exception):
    """Собственная страница 404 (подключена через handler404)."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
