import re

from django.core.exceptions import ValidationError

from core.constants import BANNED_NAMES


def username_validator(value):
    regex = r'^[\w.@+-]+\Z'
    if re.search(regex, value) is None:
        invalid_characters = set(re.findall(r'[^\w.@+-]', value))
        raise ValidationError(
            (
                f'Недопустимые символы {invalid_characters} в username. '
                'username может содержать только буквы, цифры и знаки '
                '@/./+/-/_.'
            ),
        )

    if value.lower() in BANNED_NAMES:
        raise ValidationError(
            f'Использовать имя "{value}" запрещено.'
        )
