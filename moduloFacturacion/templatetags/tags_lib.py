from django import template

register = template.Library()

#@register.inclusion_tag('ClientesFrontEnd/buscarHistoriaClinica.html')
@register.simple_tag
def encoded_id(param):
    import base64
    return base64.b64encode(str(param))

@register.simple_tag
def decode_id(param):
        import base64
        return base64.b64decode(param)