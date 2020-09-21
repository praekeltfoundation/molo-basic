from django.test import TestCase

from molo.basic.models import (
    Main, FormPage, FormIndexPage,
    SiteLanguageRelation, Languages, LanguageRelation
)

from molo.basic.tests.base import MoloTestCaseMixin


class TestFormAdmin(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()
        self.main = Main.objects.all().first()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)

        self.english = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en', is_active=True)

        LanguageRelation.objects.create(
            page=self.main, language=self.english)

        self.yourmind = self.mk_section(
            self.section_index, title='Your mind')
        self.yourmind_sub = self.mk_section(
            self.yourmind, title='Your mind subsection')

        self.admin = self.login()

    def test_form_index_page(self):
        url = '/admin/api/v2beta/pages/?child_of={}&for_explorer=1'\
            .format(self.main.pk)

        res = self.client.get(url)
        self.assertContains(res, 'Forms')

    def test_section_form_subpage(self):
        kw = {
            'title': 'Section subpage:Form'
        }
        form = FormPage(**kw)
        self.yourmind.add_child(instance=form)
        self.yourmind.save_revision().publish()

        url = '/admin/pages/{}/'.format(self.yourmind.pk)
        res = self.client.get(url)
        self.assertContains(res, kw['title'])

    def test_form_index_form_subpage(self):
        kw = {
            'title': 'Form index subpage'
        }
        form = FormPage(**kw)
        form_index = FormIndexPage.objects.filter().first()
        form_index.add_child(instance=form)
        form_index.save_revision().publish()

        url = '/admin/pages/{}/'.format(form_index.pk)
        res = self.client.get(url)
        self.assertContains(res, kw['title'])
