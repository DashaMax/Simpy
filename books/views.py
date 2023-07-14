from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'books/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['title'] = 'Simpy - главная страница'
        return context


