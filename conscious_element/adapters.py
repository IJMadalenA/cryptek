from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError

from conscious_element.views.email_validation import check_and_block_email


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        """Valida el email antes de permitir el registro"""
        email = super().clean_email(email)

        # Si el email es identificado como temporal o inválido, se bloquea y se almacena en la BD
        if check_and_block_email(email):
            raise ValidationError("The email domain is blocked. Please use a different email address.")

        return email
