import views
import django.urls
import django.views.generic

app_name = 'views'
urlpatterns = [
    django.urls.path('', django.views.generic.TemplateView.as_view(template_name='main.html')),
    
]
