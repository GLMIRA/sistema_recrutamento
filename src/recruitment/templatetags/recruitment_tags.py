from django import template

register = template.Library()


@register.filter
def verbose_name(obj, field_name):
    """retorna o verbose_name de um field

    Args:
        obj (Model): objeto Model
        field_name (str): nome field do obj

    Returns:
        str: verbose_name
    """
    return obj._meta.get_field(field_name).verbose_name


@register.filter
def display_choice(obj, field_name):
    """retorna o valor amigavel de uma choice

    Args:
        obj (Model): objeto Model
        field_name (str): nome field do obj

    Returns:
        str: valor amigavel
    """
    method = f"get_{field_name}_display"
    return getattr(obj, method)()


@register.filter
def format_date(value, date_format):
    """formata uma data no padrao informado

    Args:
        value (date): obj tipo data
        date_format (str): str de formatacao de data do padrao python

    Returns:
        str: data no formato pedido
    """
    return value.strftime(date_format)
