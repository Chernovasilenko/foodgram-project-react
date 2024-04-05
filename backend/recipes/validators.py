import re

from django.core.exceptions import ValidationError


def color_validator(value):
    """Проверяет правильность написания цвета в формате HEX."""
    regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not re.match(regex, value):
        raise ValidationError(
            'Поле должно содержать HEX-код цвета в формате #RRGGBB'
        )
