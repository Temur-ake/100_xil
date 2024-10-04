from django.template import Library

register = Library()


@register.filter()
def current_cat_slug(path: str):
    return path.split('/')[-1]


@register.filter()
def customlen(itr):
    return len(itr)


@register.filter()
def path_endswith(path: str, end: str):
    return path.endswith(end)
