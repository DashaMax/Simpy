from django import template


register = template.Library()


@register.simple_tag(name='url_path')
def url_replace(request, value):
    path = request.GET.copy()
    path['page'] = value
    return path.urlencode()