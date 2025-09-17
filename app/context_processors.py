from .models import  MainCategory


def categories_processor(request):
    return {
        'main_category': MainCategory.objects.all(),
    }