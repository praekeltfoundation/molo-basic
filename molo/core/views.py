from os import environ
import pkg_resources
import requests

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.http import is_safe_url
from django.http import JsonResponse, Http404
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied
from django.contrib.sitemaps import views as sitemap_views
from django.shortcuts import redirect, get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, get_language_from_request)

from wagtail.search.models import Query
from wagtail.core.models import Page, UserPagePermissionsProxy

from wagtail.contrib.sitemaps.sitemap_generator import Sitemap

from molo.core.utils import generate_slug, get_locale_code
from molo.core.models import (
    ArticlePage, Languages,
    SectionPage,
    TranslatablePageMixinNotRoutable)

from molo.core.known_plugins import known_plugins
from molo.core.tasks import copy_to_all_task

from el_pagination.decorators import page_template


def csrf_failure(request, reason=""):
    freebasics_url = settings.FREE_BASICS_URL_FOR_CSRF_MESSAGE
    return render(request, '403_csrf.html', {'freebasics_url': freebasics_url})


def search(request, results_per_page=10, load_more=False):
    search_query = request.GET.get('q', None)
    search_query = search_query.strip() if search_query else search_query
    page = request.GET.get('p', 1)
    locale = get_locale_code(get_language_from_request(request))

    if search_query:
        main = request.site.root_page

        results = ArticlePage.objects.descendant_of(main).filter(
            language__locale=locale
        ).exact_type(ArticlePage).values_list('pk', flat=True)

        # Elasticsearch backend doesn't support filtering
        # on related fields, at the moment.
        # So we need to filter ArticlePage entries using DB,
        # then, we will be able to search
        results = ArticlePage.objects.filter(pk__in=results)
        results = results.live().search(search_query)

        # At the moment only ES backends have highlight API.
        if hasattr(results, 'highlight'):
            results = results.highlight(
                fields={
                    'title': {},
                    'subtitle': {},
                    'body': {},
                },
                require_field_match=False
            )

        Query.get(search_query).add_hit()
    else:
        results = ArticlePage.objects.none()
    if load_more:
        return results
    paginator = Paginator(results, results_per_page)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'results': results,
    })


def locale_set(request, locale):
    request.session[LANGUAGE_SESSION_KEY] = locale
    # the next var if empty a blank is passed instead of / hence the below
    return redirect(request.GET.get('next', '/') or '/')


def health(request):
    app_id = environ.get('MARATHON_APP_ID', None)
    ver = environ.get('MARATHON_APP_VERSION', None)
    return JsonResponse({'id': app_id, 'version': ver})


def add_translation(request, page_id, locale):
    _page = get_object_or_404(Page, id=page_id)
    page = _page.specific
    if not issubclass(type(page), TranslatablePageMixinNotRoutable):
        messages.add_message(
            request, messages.INFO, _('That page is not translatable.'))
        return redirect(reverse('wagtailadmin_home'))
    # redirect to edit page if translation already exists for this locale
    translated_page = page.translated_pages.filter(language__locale=locale)
    if translated_page.exists():
        return redirect(
            reverse('wagtailadmin_pages:edit', args=[
                translated_page.first().id]))

    # create translation and redirect to edit page
    language = Languages.for_site(request.site).languages.filter(
        locale=locale).first()
    if not language:
        raise Http404
    new_title = str(language) + " translation of %s" % page.title
    new_slug = generate_slug(new_title)
    translation = page.__class__(
        title=new_title, slug=new_slug, language=language)
    page.get_parent().add_child(instance=translation)
    translation.save_revision()
    # add the translation the new way
    page.specific.translated_pages.add(translation)
    page.save()
    translation.specific.translated_pages.add(page)
    translation.save()
    for translated_page in \
            page.specific.translated_pages.all():
        translations = page.specific.translated_pages.all().\
            exclude(language__pk=translated_page.language.pk)
        for translation in translations:
            translated_page.translated_pages.add(translation)
        translated_page.save()

    # make sure new translation is in draft mode
    translation.unpublish()
    return redirect(
        reverse('wagtailadmin_pages:edit', args=[translation.id]))


def versions(request):
    comparison_url = "https://github.com/praekelt/%s/compare/%s...%s"
    plugins_info = []
    for plugin in known_plugins():
        try:
            plugin_version = (
                pkg_resources.get_distribution(plugin[0])).version

            pypi_version = get_pypi_version(plugin[0])

            if plugin[0] == 'molo.core':
                compare_versions_link = comparison_url % (
                    'molo', plugin_version, pypi_version)
            else:
                compare_versions_link = comparison_url % (
                    plugin[0], plugin_version, pypi_version)

            plugins_info.append((plugin[1], pypi_version,
                                 plugin_version, compare_versions_link))
        except:
            pypi_version = get_pypi_version(plugin[0])
            plugins_info.append((plugin[1], pypi_version, "-",
                                 ""))

    return render(request, 'versions.html', {
        'plugins_info': plugins_info,
    })


def get_pypi_version(plugin_name):
    url = "https://pypi.python.org/pypi/%s/json"
    try:
        content = requests.get(url % plugin_name).json()
        return content.get('info').get('version')
    except:
        return 'request failed'


@page_template(
    'patterns/basics/article-teasers/latest-promoted_variations/'
    'latest-articles_for-paging.html')
def home_index(
        request,
        extra_context=None,
        template=(
            'patterns/components/article-teasers/latest-promoted_variations/'
            'article_for_paging.html')):
    locale_code = request.GET.get('locale')
    return render(request, template, {'locale_code': locale_code})


@page_template(
    'patterns/basics/sections/sectionpage-article-list-'
    'standard_for-paging.html')
def section_index(
        request,
        extra_context=None,
        template=(
            'patterns/basics/sections/sectionpage-article-list-'
            'standard_for-paging.html')):
    section = SectionPage.objects.get(pk=request.GET.get('section'))
    locale_code = request.GET.get('locale')
    return render(
        request, template, {'section': section, 'locale_code': locale_code})


@page_template('search/search_results_for_paging.html')
def search_index(
        request,
        extra_context=None,
        template=('search/search_results_for_paging.html')):
    search_query = request.GET.get('q')
    results = search(request, load_more=True)
    locale_code = request.GET.get('locale')
    return render(
        request, template, {
            'search_query': search_query, 'results': results,
            'locale_code': locale_code})


@page_template(
    'patterns/basics/article-teasers/latest-promoted_variations/late'
    'st-articles_for-feature.html')
def home_more(
        request, template='core/main-feature-more.html', extra_context=None):
    locale_code = request.GET.get('locale')
    return render(request, template, {'locale_code': locale_code})


def get_valid_next_url_from_request(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if not next_url or not is_safe_url(url=next_url, host=request.get_host()):
        return ''
    return next_url


def copy_to_all_confirm(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    next_url = get_valid_next_url_from_request(request)
    if request.method == 'POST':
        if next_url:
            return redirect(next_url)
        return redirect('wagtailadmin_explore', page.get_parent().id)

    return render(request, 'wagtailadmin/pages/confirm_copy_to_all.html', {
        'page': page,
        'next': next_url,
        'not_live_descendant_count': page.get_descendants().not_live().count()
    })


def copy_to_all(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    copy_to_all_task.delay(page.pk, request.user.pk, request.site.pk)
    next_url = get_valid_next_url_from_request(request)
    if next_url:
        return redirect(next_url)
    return redirect('wagtailadmin_explore', page.get_parent().id)


def publish(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific

    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.for_page(page).can_publish():
        raise PermissionDenied

    next_url = get_valid_next_url_from_request(request)

    if request.method == 'POST':
        include_descendants = request.POST.get("include_descendants", False)

        page.save_revision().publish()

        if include_descendants:
            not_live_descendant_pages = (
                page.get_descendants().not_live().specific())
            for not_live_descendant_page in not_live_descendant_pages:
                if user_perms.for_page(not_live_descendant_page).can_publish():
                    not_live_descendant_page.save_revision().publish()

        if next_url:
            return redirect(next_url)
        return redirect('wagtailadmin_explore', page.get_parent().id)

    return render(request, 'wagtailadmin/pages/confirm_publish.html', {
        'page': page,
        'next': next_url,
        'not_live_descendant_count': page.get_descendants().not_live().count()
    })


class MoloSitemap(Sitemap):
    def _urls(self, page, protocol, domain):
        urls = []
        last_mods = set()

        for item in self.paginator.page(page).object_list:

            url_info_items = item.get_sitemap_urls()

            for url_info in url_info_items:
                urls.append(url_info)
                last_mods.add(url_info.get('lastmod'))

        # last_mods might be empty if the whole site is private
        if last_mods and None not in last_mods:
            self.latest_lastmod = max(last_mods)
        return urls


def sitemap(request, **kwargs):
    sitemaps = {'wagtail': MoloSitemap(request)}
    return sitemap_views.sitemap(request, sitemaps, **kwargs)
