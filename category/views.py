from django.http import HttpResponse


def category_list(request):
    return HttpResponse("Список категорий")


def category_detail(request, category_id):
    return HttpResponse(f"Категория {category_id}")
