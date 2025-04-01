import dns.resolver
import environ
import requests
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError

from user_app.models.blocked_email_domain import (BlockedEmailDomain,
                                                  BlockedEmailDomainExtension)

HUNTER_API_KEY = environ.Env().str("HUNTER_API_KEY")


def email_is_legitimate(email):
    """
    Verifies if an email is legitimate based on multiple criteria:
    - Hunter.io API analysis.
    - Valid MX records.
    - Database checks for blocked domains.

    Returns True if the email is legitimate, otherwise False.
    """

    # Extract the domain from the email (handle domains with subdomains or double extensions like "gov.es")
    username, domain = email.split("@")
    base_domain = domain.split(".")[0]
    domain_extension = domain.split(".")[1:]
    domain_extension = ".".join(domain_extension)

    # Database Check - If the domain or its base is blocked
    if BlockedEmailDomain.objects.filter(domain__in=[domain, base_domain]).exists():
        return False

    # HUNTER.IO API Call
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}")
    data = response.json().get("data", {})
    is_disposable = data.get("disposable", True)
    smtp_check = data.get("smtp_check", False)
    mx_records_from_hunter = data.get("mx_records", False)
    score = data.get("score", 0)
    status = data.get("status", "invalid")

    # Evaluate the overall legitimacy
    if is_disposable or not smtp_check or not mx_records_from_hunter or score < 80 or status != "valid":
        _block_domain(username, base_domain, domain_extension)  # Block the domain if illegitimate
        return False

    # MX Check using DNS (double-check independently)
    try:
        mx_records = dns.resolver.resolve(domain, "MX")
        has_valid_mx_records = len(mx_records) > 0
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        has_valid_mx_records = False

    # Final validation check combining Hunter.io and DNS
    if not has_valid_mx_records:
        _block_domain(username, base_domain, domain_extension)
        return False

    return True


def _block_domain(username, domain, extension):
    """
    Helper function to block a domain by adding it to the BlockedEmailDomain database.
    """
    # Ensure correct handling of domain extensions
    print("Blocking domain:", domain)
    print("Domain extension:", extension)
    domain_ext, _ = BlockedEmailDomainExtension.objects.get_or_create(domain_extension=extension)
    if not BlockedEmailDomain.objects.filter(domain=domain).exists():
        BlockedEmailDomain.objects.create(username=username, domain=domain, domain_extension=domain_ext)


class CustomAccountAdapter(DefaultAccountAdapter):

    def clean_email(self, email):
        """Valida el email antes de permitir el registro"""
        email = super().clean_email(email)

        # Si el email es identificado como temporal o inválido, se bloquea y se almacena en la BD
        if email_is_legitimate(email):
            raise ValidationError("The email domain is blocked. Please use a different email address.")

        return email
