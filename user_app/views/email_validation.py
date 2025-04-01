import dns.resolver
import environ
import requests

from user_app.models.blocked_email_domain import BlockedEmailDomain, BlockedEmailDomainExtension

HUNTER_API_KEY = environ.Env().str("HUNTER_API_KEY")


def extract_base_domain(email):
    """Extrae el dominio base sin importar el TLD. Ej: temp-mail.abc → temp-mail"""
    domain = email.split("@")[-1].lower()
    parts = domain.split(".")
    return ".".join(parts[:-1]) if len(parts) > 2 else domain


def is_temporary_email(email):
    """Verifica si el email es temporal usando la API de Hunter.io"""
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}")
    data = response.json()
    return data.get("data", {}).get("disposable", False)


def has_valid_mx_records(domain):
    """Verifica si el dominio tiene registros MX válidos"""
    try:
        records = dns.resolver.resolve(domain, "MX")
        return len(records) > 0
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False


def is_blocked_domain(email):
    """Verifica si el dominio (o su base) está bloqueado en la BD"""
    domain = email.split("@")[-1].lower()
    base_domain = extract_base_domain(email)

    return BlockedEmailDomain.objects.filter(domain__in=[domain, base_domain]).exists()


def add_blocked_domain(email):
    """Añade un dominio a la base de datos de bloqueados"""
    username, domain = email.split("@")
    extension = domain.split(".")[-1]

    # Verificar si la extensión ya está en la BD
    domain_ext, _ = BlockedEmailDomainExtension.objects.get_or_create(domain_extension=extension)

    # Verificar si el dominio ya está en la BD
    if not BlockedEmailDomain.objects.filter(domain=domain).exists():
        BlockedEmailDomain.objects.create(username=username, domain=domain, domain_extension=domain_ext)


def check_and_block_email(email):
    """Verifica si un email es temporal o inválido y lo bloquea si es necesario"""
    domain = email.split("@")[-1]

    # Si el dominio ya está bloqueado, no hacemos nada
    if is_blocked_domain(email):
        return True

    # Verificamos con la API externa
    if is_temporary_email(email) or not has_valid_mx_records(domain):
        add_blocked_domain(email)  # Guardar en la base de datos
        return True  # Bloquear email

    return False  # Email válido
