from django.conf import settings


def company_info(request):
    """
    Context processor pour rendre les informations de l'entreprise
    disponibles dans tous les templates
    """
    return {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_SHORT_NAME': settings.COMPANY_SHORT_NAME,
        'COMPANY_RCCM': settings.COMPANY_RCCM,
        'COMPANY_NIF': settings.COMPANY_NIF,
        'COMPANY_TVA': settings.COMPANY_TVA,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_PHONE_2': settings.COMPANY_PHONE_2,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'COMPANY_WEBSITE': settings.COMPANY_WEBSITE,
        'CURRENCY': settings.CURRENCY,
        'CURRENCY_SYMBOL': settings.CURRENCY_SYMBOL,
    }
