from django import template
from django.contrib.contenttypes.models import ContentType

from likes.models import LikeModel

register = template.Library()


@register.simple_tag(name='like_user')
def get_like(user, pk):
    like_user = LikeModel.objects.filter(
        user=user,
        object_id=pk,
        content_type=ContentType.objects.get(model='blogmodel')
    )

    if like_user:
        return like_user[0]

    return None