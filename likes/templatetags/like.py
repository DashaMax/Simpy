from django import template
from django.contrib.contenttypes.models import ContentType

from likes.models import LikeModel


MODEL = {
    'quote': 'quotemodel',
    'blog': 'blogmodel',
}

register = template.Library()


@register.simple_tag(name='like_user')
def get_like(model, user, pk):
    like_user = LikeModel.objects.filter(
        user=user,
        object_id=pk,
        content_type=ContentType.objects.get(model=MODEL[model])
    )

    if like_user:
        return like_user[0]