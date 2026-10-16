"""Корневая маршрутизация Django-проекта InquiryDesk.

Адреса распределяются между приложениями функцией include(): здесь указан
префикс адреса, а оставшаяся часть ищется в urls.py приложения.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("inquiries/", include("inquiry.urls")),
    path("categories/", include("category.urls")),
]
