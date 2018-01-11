from django import template

register = template.Library()


@register.filter(name='addclass')
def add_class(value, arg):
    """
    :type value: django.forms.boundfield.BoundField
    :type arg: str
    """
    return value.as_widget(attrs={'class': arg})


@register.filter(name='severity')
def table_severity(value):
    if value > 5:
        return "table-danger"
    elif value > 3:
        return "table-warning"
    else:
        return ""

@register.filter(name='security')
def security(value):
    value = float(value)
    if value >= 0.5:
        return "primary"
    elif value >= 0.1:
        return "warning"
    else:
        return "danger"

@register.filter(name='nonzero')
def non_zero(value):
    return "" if value == 0 else value
