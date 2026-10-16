from django.http import HttpResponse


def index(request):
    return HttpResponse("InquiryDesk – система регистрации обращений")
