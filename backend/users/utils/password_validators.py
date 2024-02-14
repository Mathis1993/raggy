from django.core.exceptions import ValidationError
from django.utils.translation import ngettext_lazy


class ContainsUppercaseValidator:
    def __init__(self, min_uppercase: int = 1):
        self.min_upper = min_uppercase

    def validate(self, password, user=None):
        if sum(c.isupper() for c in password) < self.min_upper:
            raise ValidationError(
                f"Password must contain at least {self.min_upper} uppercase character.",
                code="password_no_upper",
            )

    def get_help_text(self):
        return f"Your password must contain at least {self.min_upper} uppercase character."


class ContainsLowercaseValidator:
    def __init__(self, min_lowercase: int = 1):
        self.min_lower = min_lowercase

    def validate(self, password, user=None):
        if sum(c.islower() for c in password) < self.min_lower:
            raise ValidationError(
                f"Password must contain at least {self.min_lower} lowercase character.",
                code="password_no_lower",
            )

    def get_help_text(self):
        return f"Your password must contain at least {self.min_lower} lowercase character."


class SpecialCharacterValidator:
    def __init__(self, min_special: int = 1):
        self.min_special = min_special

    def validate(self, password, user=None):
        special_characters = "!@#$%^&*()-_+=[]{}|;:,.<>?/`~"
        if sum(c in special_characters for c in password) < self.min_special:
            raise ValidationError(
                f"Password must contain at least {self.min_special} special character.",
                code="password_no_special",
            )

    def get_help_text(self):
        return f"Your password must contain at least {self.min_special} special character."
