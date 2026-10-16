"""View-функции приложения inquiry: список и карточка обращения (ПР5).

Данные загружаются из JSON средствами ПР3 (storage.py), поиск и сортировка
выполняются функциями модуля inquiries.py.
"""

from django.http import HttpResponse
from django.utils.html import escape

import inquiries as inquiries_module
import storage
from homepage.views import page, status_badge


def inquiry_items(inquiries):
    """Сформировать HTML-список обращений со ссылками на их карточки."""
    if not inquiries:
        return '<p class="text-body-secondary">Обращений пока нет.</p>'
    items = ""
    for inquiry in inquiries_module.sort_inquiries_by_date(inquiries):
        author = escape(inquiry.author.name) if inquiry.author else "—"
        items += f"""
        <a href="/inquiries/{inquiry.id}/"
           class="list-group-item list-group-item-action">
            <div class="d-flex justify-content-between">
                <span class="fw-semibold">{escape(inquiry.subject)}</span>
                {status_badge(inquiry.status)}
            </div>
            <small class="text-body-secondary">
                №{inquiry.id} · {inquiry.created} · {author}
            </small>
        </a>"""
    return f'<div class="list-group">{items}</div>'


def inquiry_list(request):
    _, _, _, inquiries = storage.load_all()
    content = f"""
    <h1 class="mb-3">Обращения</h1>
    <p class="text-body-secondary">Всего: {len(inquiries)},
        сначала новые.</p>
    {inquiry_items(inquiries)}
    """
    return HttpResponse(page("InquiryDesk – обращения", content))


def inquiry_detail(request, inquiry_id):
    _, _, _, inquiries = storage.load_all()
    inquiry = inquiries_module.find_inquiry(inquiries, inquiry_id)

    if inquiry is None:
        content = """
        <h1 class="text-danger">Обращение не найдено</h1>
        <a href="/inquiries/" class="btn btn-outline-secondary">
            ← к списку обращений
        </a>
        """
        return HttpResponse(
            page("Обращение не найдено", content),
            status=404,
        )

    if inquiry.category is not None:
        category = (
            f'<a href="/categories/{inquiry.category.id}/">'
            f"{escape(inquiry.category.name)}</a>"
        )
    else:
        category = "—"
    author = escape(inquiry.author.name) if inquiry.author else "—"
    text = escape(inquiry.text) or "<em>описание не указано</em>"
    state = "завершена" if inquiry.is_closed() else "продолжается"

    content = f"""
    <div class="card">
        <div class="card-header">Обращение №{inquiry.id}</div>
        <div class="card-body">
            <h1 class="card-title h4">{escape(inquiry.subject)}</h1>
            <p class="card-text">{text}</p>
            <dl class="row mb-0">
                <dt class="col-sm-3">Статус</dt>
                <dd class="col-sm-9">{status_badge(inquiry.status)}</dd>
                <dt class="col-sm-3">Обработка</dt>
                <dd class="col-sm-9">{state}</dd>
                <dt class="col-sm-3">Категория</dt>
                <dd class="col-sm-9">{category}</dd>
                <dt class="col-sm-3">Автор</dt>
                <dd class="col-sm-9">{author}</dd>
                <dt class="col-sm-3">Дата регистрации</dt>
                <dd class="col-sm-9">{inquiry.created}</dd>
            </dl>
        </div>
        <div class="card-footer bg-transparent">
            <a href="/inquiries/" class="btn btn-outline-secondary">
                ← к списку обращений
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Обращение №{inquiry.id}", content),
        status=200,
    )
