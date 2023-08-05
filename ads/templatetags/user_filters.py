from django import template


# To use the gravatar filter in a template include
# {% load user_filters %}

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
