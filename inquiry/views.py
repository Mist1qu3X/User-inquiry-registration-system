from django.http import HttpResponse


def inquiry_list(request):
    return HttpResponse("Список обращений")


def inquiry_detail(request, inquiry_id):
    return HttpResponse(f"Обращение {inquiry_id}")
