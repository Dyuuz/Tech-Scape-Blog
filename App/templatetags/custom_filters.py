from django import template
import math

register = template.Library()

# Custom template tag to perform arithmetical ops
@register.filter(name='divide_by')
def divide_by(value, arg):
    """Divides the value by the argument."""
    try:
        return math.floor(value / arg)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter(name='floatformat')
def floatformat(value, arg):
    """Floor the value"""
    try:
        return math.floor(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter(name='lowercasepyt')
def lowercasepyt(text):
    """Change the value to lowercase"""
    try:
        return text.lower()
    except:
        return None

@register.filter(name='split_text')
def split_text(body, max_length):
    """Change the words to a specific list"""
    try:
        if len(body) > max_length:
            truncated_body = body[:max_length].rsplit(' ', 1)[0]
        
        return truncated_body
    except:
        return None