from django.core.exceptions import ValidationError
import re

class NumberValidator:
    def validate(self, password, user=None):
        if not re.search(r"\d", password):
            raise ValidationError(
                "The password must contain at least one digit.",
                code="password_no_number",
            )

    def get_help_text(self):
        return "Your password must contain at least one digit."