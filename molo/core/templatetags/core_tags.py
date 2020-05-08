from itertools import chain
from markdown import markdown

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django import template
from django.utils.safestring import mark_safe
from django.db.models import Case, When

from prometheus_client import Summary

from molo.core.decorators import prometheus_query_count
from molo.core.models import (
    Page, ArticlePage, SectionPage, SiteSettings, Languages,
    SectionIndexPage,
    BannerPage, get_translation_for,
    ArticleOrderingChoices
)


register = template.Library()


REQUEST_TIME = Summary(
        'request_processing_seconds', 'Time spent processing request')


def get_language(site, locale):
    language_cache_key = 'get_pages_language_{}_{}'.format(site.pk, locale)
    language = cache.get(language_cache_key)
    if not language:
        language = Languages.for_site(site).languages.filter(
            locale=locale).first()
        cache.set(language_cache_key, language, None)
    return language


def get_pages(context, queryset, locale):
    from molo.core.models import get_translation_for

    if queryset.count() == 0:
        return []

    request = context['request']
    if not hasattr(request, 'site'):
        return list[queryset]

    language = get_language(request.site, locale)
    if language and language.is_main_language:
        return list(queryset.live())
    pages = get_translation_for(queryset, locale, request.site)
    return pages or []


@register.simple_tag(takes_context=True)
def load_sections(context, service_aggregator=False):
    request = context['request']
    locale = context.get('locale_code')
    if request.site:
        qs = request.site.root_page.specific.sections().filter(
            is_service_aggregator=service_aggregator)
    else:
        return []
    return get_pages(context, qs, locale)


@register.simple_tag(takes_context=True)
def get_translation(context, page):
    try:
        return page.translated_pages.get(
            language__locale=context.get('locale_code'))
    except:
        return page


@register.simple_tag(takes_context=True)
def get_parent(context, page):
    parent = page.get_parent()
    if not parent.specific_class == SectionIndexPage:
        return get_translation(context, parent.specific)
    return None


@register.inclusion_tag(
    'core/tags/section_listing_homepage.html',
    takes_context=True
)
def section_listing_homepage(context):
    locale_code = context.get('locale_code')
    return {
        'sections': load_sections(context),
        'request': context['request'],
        'locale_code': locale_code,
    }


@register.inclusion_tag(
    'core/tags/latest_listing_homepage.html',
    takes_context=True
)
def latest_listing_homepage(context, num_count=5):
    request = context['request']
    locale = context.get('locale_code')

    if request.site:
        articles = request.site.root_page.specific.latest_articles()
    else:
        articles = []
    return {
        'articles': get_pages(context, articles, locale)[:num_count],
        'request': context['request'],
        'locale_code': locale,
    }


@register.inclusion_tag(
    'core/tags/hero_article.html',
    takes_context=True
)
def hero_article(context):
    request = context['request']
    locale = context.get('locale_code')

    if request.site:
        articles = request.site.root_page.specific \
            .hero_article()
    else:
        articles = ArticlePage.objects.none()

    return {
        'articles': get_pages(context, articles, locale),
        'request': context['request'],
        'locale_code': locale,
    }


@register.inclusion_tag('core/tags/bannerpages.html', takes_context=True)
def bannerpages(context, position=-1):
    pages = []
    request = context['request']
    locale = context.get('locale_code')

    if request.site:
        pages = request.site.root_page.specific.bannerpages().exact_type(
            BannerPage)

    if position >= 0:
        banners = get_pages(context, pages, locale)
        if position > (len(banners) - 1):
            return None

        if banners and len(banners) > position:
            return {
                'bannerpages': [banners[position]],
                'request': context['request'],
                'locale_code': locale,
                'is_via_freebasics':
                    'Internet.org' in request.META.get('HTTP_VIA', '') or
                    'InternetOrgApp' in request.META.get(
                        'HTTP_USER_AGENT', '') or
                    'true' in request.META.get('HTTP_X_IORG_FBS', '')
            }
        return None
    return {
        'bannerpages': get_pages(context, pages, locale),
        'request': context['request'],
        'locale_code': locale,
        'is_via_freebasics':
            'Internet.org' in request.META.get('HTTP_VIA', '') or
            'InternetOrgApp' in request.META.get('HTTP_USER_AGENT', '') or
            'true' in request.META.get('HTTP_X_IORG_FBS', '')
    }


@register.inclusion_tag('core/tags/footerpage.html', takes_context=True)
def footer_page(context):
    pages = []
    request = context['request']
    locale = context.get('locale_code')

    if request.site:
        pages = request.site.root_page.specific.footers()

    return {
        'request': request,
        'locale_code': locale,
        'footers': get_pages(context, pages, locale),
    }


@register.inclusion_tag('core/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    translated_ancestors = []
    self = context.get('self')
    locale_code = context.get('locale_code')

    if self is not None and not self.depth <= 2:
        ancestors = Page.objects.live().ancestor_of(
            self, inclusive=True).filter(depth__gt=3)
        if ancestors:
            translated_ancestors = get_pages(context, ancestors, locale_code)

    return {
        'ancestors': translated_ancestors,
        'request': context['request'],
    }


@register.inclusion_tag(
    'wagtail/translations_actions.html', takes_context=True)
def render_translations(context, page):
    from molo.core.models import TranslatablePageMixinNotRoutable
    if not issubclass(type(page.specific), TranslatablePageMixinNotRoutable):
        return {}
    if not page.specific.language.is_main_language:
        return {}

    languages = [
        (l.locale, str(l))
        for l in Languages.for_site(
            context['request'].site.root_page.get_site()).languages.filter(
                is_main_language=False)]

    translated = []
    for code, title in languages:
        translated.append({
            'locale': {'title': title, 'code': code},
            'translated':
                page.specific.translated_pages.filter(
                    language__locale=code).first() or []})

    return {
        'translations': translated,
        'page': page
    }


@register.simple_tag(takes_context=True)
def load_descendant_articles_for_section(
        context, section, featured_in_homepage=None, featured_in_section=None,
        featured_in_latest=None, count=5):
    """
    Returns all descendant articles (filtered using the parameters)
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    """
    request = context.get('request')
    locale = context.get('locale_code')
    page = section.get_main_language_page()
    settings = SiteSettings.for_site(request.site) \
        if request else None

    qs = ArticlePage.objects.descendant_of(page).filter(
        language__is_main_language=True)

    article_ordering = getattr(
        settings, 'article_ordering_within_section', None)

    if article_ordering:
        order_by = ArticleOrderingChoices.\
            get(settings.article_ordering_within_section).name.lower()

        order_by = order_by if order_by.find('_desc') == -1 \
            else '-{}'.format(order_by.replace('_desc', ''))

        # if the sort order is equal to CMS_DEFAULT_SORTING
        #  do not order QS, CMS handles it
        if article_ordering != ArticleOrderingChoices.CMS_DEFAULT_SORTING:
            qs = qs.order_by(order_by)

    if featured_in_homepage:
        qs = qs.filter(featured_in_homepage=featured_in_homepage)\
            .order_by('-featured_in_homepage_start_date')

    if featured_in_latest:
        qs = qs.filter(featured_in_latest=featured_in_latest)

    if featured_in_section:
        qs = qs.filter(featured_in_section=featured_in_section)\
            .order_by('-featured_in_section_start_date')

    if not locale:
        return qs.live()[:count]

    return get_pages(context, qs, locale)[:count]


@register.simple_tag(takes_context=True)
def load_child_articles_for_section(
        context, section, featured_in_section=None, count=5):
    """
    Returns all child articles
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    """
    if not section:
        return None
    request = context.get('request')
    locale = context.get('locale_code')
    main_language_page = section.specific.get_main_language_page()
    settings = SiteSettings.for_site(request.site) \
        if request else None

    # TODO: Consider caching the pks of these articles using a timestamp on
    # section as the key so tha twe don't always do these joins
    article_ordering = getattr(
        settings, 'article_ordering_within_section', None)
    order_by = ArticleOrderingChoices.\
        get(settings.article_ordering_within_section).name.lower() \
        if article_ordering else '-first_published_at'

    order_by = order_by if order_by.find('_desc') == -1 \
        else '-{}'.format(order_by.replace('_desc', ''))

    child_articles = ArticlePage.objects.child_of(
        main_language_page).filter(
        language__is_main_language=True)

    # if the sort order is equal to CMS_DEFAULT_SORTING
    #  do not order QS, CMS handles it
    if article_ordering != ArticleOrderingChoices.CMS_DEFAULT_SORTING:
        child_articles = child_articles.order_by(order_by)

    if featured_in_section is not None:
        child_articles = child_articles.filter(
            featured_in_section=featured_in_section)\
            .order_by('-featured_in_section_start_date')

    related_articles = ArticlePage.objects.filter(
        related_sections__section__slug=main_language_page.slug)
    qs = list(chain(
        get_pages(context, child_articles, locale),
        get_pages(context, related_articles, locale)))

    # Pagination
    if count:
        p = context.get('p', 1)
        paginator = Paginator(qs, count)

        try:
            articles = paginator.page(p)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
    else:
        articles = qs
    if not locale:
        return articles

    context.update({'articles_paginated': articles})
    return articles


@prometheus_query_count
@register.simple_tag(takes_context=True)
def load_child_sections_for_section(context, section, count=None):
    """
    Returns all child sections
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    """
    if not section:
        return None

    locale = context.get('locale_code')
    page = section.get_main_language_page() \
        if hasattr(section, 'get_main_language_page') else section

    qs = SectionPage.objects.child_of(page).filter(
        language__is_main_language=True)

    if not locale:
        return qs[:count]
    return get_pages(context, qs, locale)


@prometheus_query_count
@register.simple_tag(takes_context=True)
def load_sibling_sections(context, section, count=None):
    """
    Returns all sibling sections
    If the `locale_code` in the context is not the main language, it will
    return the translations of the live articles.
    """
    page = section.get_main_language_page()
    locale = context.get('locale_code')

    qs = SectionPage.objects.sibling_of(page).filter(
        language__is_main_language=True)

    if not locale:
        return qs[:count]
    return get_pages(context, qs, locale)


@register.filter
def handle_markdown(value):
    md = markdown(
        value,
        extensions=[
            'markdown.extensions.fenced_code',
            'codehilite',
        ]
    )
    """ For some unknown reason markdown wraps the value in <p> tags.
        Currently there doesn't seem to be an extension to turn this off.
    """
    open_tag = '<p>'
    close_tag = '</p>'
    if md.startswith(open_tag) and md.endswith(close_tag):
        md = md[len(open_tag):-len(close_tag)]
    return mark_safe(md)


@prometheus_query_count
@register.inclusion_tag(
    'core/tags/social_media_footer.html',
    takes_context=True
)
def social_media_footer(context, page=None):
    locale = context.get('locale_code')
    social_media = SiteSettings.for_site(context['request'].site).\
        social_media_links_on_footer_page

    data = {
        'social_media': social_media,
        'request': context['request'],
        'locale_code': locale,
        'page': page,
    }
    return data


@prometheus_query_count
@register.inclusion_tag(
    'core/tags/social_media_article.html',
    takes_context=True
)
def social_media_article(context, page=None):
    locale = context.get('locale_code')
    site_settings = SiteSettings.for_site(context['request'].site)
    viber = False
    twitter = False
    facebook = False
    whatsapp = False
    telegram = False

    if site_settings:
        facebook = site_settings.facebook_image
        twitter = site_settings.twitter_image
        whatsapp = site_settings.whatsapp_image
        viber = site_settings.viber_image
        telegram = site_settings.telegram_image

    data = {
        'page': page,
        'viber': viber,
        'twitter': twitter,
        'facebook': facebook,
        'whatsapp': whatsapp,
        'telegram': telegram,
        'locale_code': locale,
        'request': context['request'],
    }
    return data


@prometheus_query_count
@register.simple_tag(takes_context=True)
def get_next_article(context, article):
    locale_code = context.get('locale_code')
    section = article.get_parent_section()
    articles = load_child_articles_for_section(context, section, count=None)
    article_len = len(articles)

    if article_len > 1:
        try:
            if article_len > articles.index(article) + 1:
                next_article = articles[articles.index(article) + 1]
            else:
                next_article = articles[0]

            try:
                return next_article.translated_pages.get(
                    language__locale=locale_code)
            except:
                if next_article.language.locale == locale_code or not \
                    SiteSettings.for_site(
                        context['request'].site).show_only_translated_pages:
                    return next_article

        except ValueError:
            return None
    return None


@prometheus_query_count
@register.simple_tag(takes_context=True)
def get_recommended_articles(context, article):
    results = []
    locale_code = context.get('locale_code')

    if article.recommended_articles.exists():
        queryset = article.recommended_articles.all()\
            .values_list('recommended_article', flat=True)
    else:
        queryset = article.get_main_language_page().specific.\
            recommended_articles.all()\
            .values_list('recommended_article', flat=True)

    if queryset:
        preserved = Case(*[
            When(pk=pk, then=pos) for pos, pk in enumerate(queryset)
        ])
        articles = ArticlePage.objects\
            .filter(pk__in=queryset).order_by(preserved)

        results = get_pages(context, articles, locale_code)
    return results


@register.simple_tag(takes_context=True)
def should_hide_delete_button(context, page):
    return hasattr(page.specific, 'hide_delete_button')
