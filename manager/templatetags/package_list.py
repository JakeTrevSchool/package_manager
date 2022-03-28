from django import template

register = template.Library()


@register.inclusion_tag('manager/package_list.html', takes_context=True)
def list_packages(context):
    return {
        "packages": context['packages'],
        "pagination_url": context['pagination_url'],
        "pages_before": context['pages_before'],
        "pages_after": context['pages_after'],
        "pages": context['pages'],
        "current_page": context['page'],
        "list_null_message": context['list_null_message'],
    }
