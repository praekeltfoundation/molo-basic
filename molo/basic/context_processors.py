from django.utils.translation import get_language_from_request
from molo.basic.utils import get_locale_code
from molo.basic.models import Languages


def locale(request):
    locale_code = get_locale_code(get_language_from_request(request))
    languages = Languages.for_site(request.site).languages.filter(
        is_active=True)
    return {
        'locale_code': locale_code,
        'languages': languages,
        'selected_language': languages.filter(locale=locale_code).first()}
