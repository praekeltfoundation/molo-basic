# Generated by Django 2.2.11 on 2020-03-28 21:13

from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import modelcluster.contrib.taggit
import modelcluster.fields
import molo.core.blocks
import molo.core.mixins
import molo.core.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locale', models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dsb', 'Lower Sorbian'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hsb', 'Upper Sorbian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kab', 'Kabyle'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmål'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zu', 'Zulu'), ('xh', 'Xhosa'), ('st', 'Sotho'), ('ve', 'Venda'), ('tn', 'Tswana'), ('ts', 'Tsonga'), ('ss', 'Swati'), ('nr', 'Ndebele')], help_text='Site language', max_length=255, verbose_name='language name')),
                ('is_main_language', models.BooleanField(default=False, editable=False, verbose_name='main Language')),
                ('is_active', models.BooleanField(default=True, verbose_name='active Language')),
            ],
            options={
                'verbose_name': 'Language',
            },
        ),
        migrations.CreateModel(
            name='Timezone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoloPage',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.TextField(blank=True, null=True)),
                ('uuid', models.CharField(blank=True, max_length=32, null=True)),
                ('featured_in_latest', models.BooleanField(default=False, help_text='Article to be featured in the Latest module')),
                ('featured_in_latest_start_date', models.DateTimeField(blank=True, null=True)),
                ('featured_in_latest_end_date', models.DateTimeField(blank=True, null=True)),
                ('featured_in_section', models.BooleanField(default=False, help_text='Article to be featured in the Section module')),
                ('featured_in_section_start_date', models.DateTimeField(blank=True, null=True)),
                ('featured_in_section_end_date', models.DateTimeField(blank=True, null=True)),
                ('featured_in_homepage', models.BooleanField(default=False, help_text='Article to be featured in the Homepage within the Section module')),
                ('featured_in_homepage_start_date', models.DateTimeField(blank=True, null=True)),
                ('featured_in_homepage_end_date', models.DateTimeField(blank=True, null=True)),
                ('social_media_title', models.TextField(blank=True, null=True, verbose_name='title')),
                ('social_media_description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', molo.core.blocks.MarkDownBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='Item'))), ('numbered_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='Item'))), ('page', wagtail.core.blocks.PageChooserBlock()), ('richtext', wagtail.core.blocks.RichTextBlock()), ('html', wagtail.core.blocks.RawHTMLBlock())], blank=True, null=True)),
                ('feature_as_hero_article', models.BooleanField(default=False, help_text='Article to be featured as the Hero Article')),
                ('promote_date', models.DateTimeField(blank=True, null=True)),
                ('demote_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SiteLanguage')),
            ],
            options={
                'verbose_name': 'Article',
                'ordering': ('-latest_revision_created_at',),
            },
            bases=(molo.core.models.ImportableMixin, molo.core.models.TranslatablePageMixin, molo.core.mixins.PageEffectiveImageMixin, 'core.molopage'),
        ),
        migrations.CreateModel(
            name='BannerIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.molopage', molo.core.models.PreventDeleteMixin, molo.core.models.ImportableMixin),
        ),
        migrations.CreateModel(
            name='FooterIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.molopage', molo.core.models.PreventDeleteMixin),
        ),
        migrations.CreateModel(
            name='LanguagePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('code', models.CharField(help_text='The language code as specified in iso639-2', max_length=255)),
            ],
            options={
                'verbose_name': 'Language',
            },
            bases=('core.molopage',),
        ),
        migrations.CreateModel(
            name='Main',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.molopage',),
        ),
        migrations.CreateModel(
            name='SectionIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.molopage', molo.core.models.PreventDeleteMixin),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ga_tag_manager', models.CharField(blank=True, help_text='Local GA Tag Manager tracking code (e.g GTM-XXX) to be used to view analytics on this site only', max_length=255, null=True, verbose_name='Local GA Tag Manager')),
                ('global_ga_tag_manager', models.CharField(blank=True, help_text='Global GA Tag Manager tracking code (e.g GTM-XXX) to be used to view analytics on more than one site globally', max_length=255, null=True, verbose_name='Global GA Tag Manager')),
                ('google_search_console', models.CharField(blank=True, help_text='The Google Search Console verification code', max_length=255, null=True, verbose_name='Google Search Console')),
                ('fb_analytics_app_id', models.CharField(blank=True, help_text='The tracking ID to be used to view Facebook Analytics', max_length=25, null=True, verbose_name='Facebook Analytics App ID')),
                ('local_ga_tracking_code', models.CharField(blank=True, help_text='Local GA tracking code to be used to view analytics on this site only', max_length=255, null=True, verbose_name='Local GA Tracking Code')),
                ('global_ga_tracking_code', models.CharField(blank=True, help_text='Global GA tracking code to be used to view analytics on more than one site globally', max_length=255, null=True, verbose_name='Global GA Tracking Code')),
                ('show_only_translated_pages', models.BooleanField(default=False, help_text='When selecting this option, untranslated pages will not be visible to the front end user when they viewing a child language of the site')),
                ('time', wagtail.core.fields.StreamField([('time', wagtail.core.blocks.TimeBlock(required=False))], blank=True, help_text='The time/s content will be rotated', null=True)),
                ('monday_rotation', models.BooleanField(default=False, verbose_name='Monday')),
                ('tuesday_rotation', models.BooleanField(default=False, verbose_name='Tuesday')),
                ('wednesday_rotation', models.BooleanField(default=False, verbose_name='Wednesday')),
                ('thursday_rotation', models.BooleanField(default=False, verbose_name='Thursday')),
                ('friday_rotation', models.BooleanField(default=False, verbose_name='Friday')),
                ('saturday_rotation', models.BooleanField(default=False, verbose_name='Saturday')),
                ('sunday_rotation', models.BooleanField(default=False, verbose_name='Sunday')),
                ('content_rotation_start_date', models.DateTimeField(blank=True, help_text='The date rotation will begin', null=True)),
                ('content_rotation_end_date', models.DateTimeField(blank=True, help_text='The date rotation will end', null=True)),
                ('social_media_links_on_footer_page', wagtail.core.fields.StreamField([('social_media_site', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock())]))], blank=True, null=True)),
                ('facebook_sharing', models.BooleanField(default=False, help_text='Enable this field to allow for sharing to Facebook.', verbose_name='Facebook')),
                ('twitter_sharing', models.BooleanField(default=False, help_text='Enable this field to allow for sharing to Twitter.', verbose_name='Twitter')),
                ('whatsapp_sharing', models.BooleanField(default=False, help_text='Enable this field to allow for sharing to Whatsapp.', verbose_name='Whatsapp')),
                ('viber_sharing', models.BooleanField(default=False, help_text='Enable this field to allow for sharing to Viber.', verbose_name='Viber')),
                ('telegram_sharing', models.BooleanField(default=False, help_text='Enable this field to allow for sharing to Telegram.', verbose_name='Telegram')),
                ('article_ordering_within_section', django_enumfield.db.fields.EnumField(blank=True, default=None, enum=molo.core.models.ArticleOrderingChoices, help_text='Ordering of articles within a section', null=True)),
                ('facebook_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
                ('telegram_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('twitter_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('viber_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('whatsapp_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='wagtailcore.Page')),
                ('translated_page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='source_page', to='wagtailcore.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LanguageRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.SiteLanguage')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='wagtailcore.Page')),
            ],
        ),
        migrations.CreateModel(
            name='ImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_hash', models.CharField(max_length=256, null=True)),
                ('image', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_info', to='wagtailimages.Image')),
            ],
        ),
        migrations.CreateModel(
            name='CmsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
                ('timezone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Timezone')),
            ],
            options={
                'verbose_name': 'CMS settings',
            },
        ),
        migrations.CreateModel(
            name='FooterPage',
            fields=[
                ('articlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ArticlePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.articlepage',),
        ),
        migrations.CreateModel(
            name='SiteLanguageRelation',
            fields=[
                ('sitelanguage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SiteLanguage')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('language_setting', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='core.Languages')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('core.sitelanguage', models.Model),
        ),
        migrations.CreateModel(
            name='SectionPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', models.TextField(blank=True, null=True)),
                ('uuid', models.CharField(blank=True, max_length=32, null=True)),
                ('extra_style_hints', models.TextField(blank=True, default='', help_text='Styling options that can be applied to this section and all its descendants', null=True)),
                ('time', wagtail.core.fields.StreamField([('time', wagtail.core.blocks.TimeBlock(required=False))], blank=True, help_text='The time/s content will be rotated', null=True)),
                ('monday_rotation', models.BooleanField(default=False, verbose_name='Monday')),
                ('tuesday_rotation', models.BooleanField(default=False, verbose_name='Tuesday')),
                ('wednesday_rotation', models.BooleanField(default=False, verbose_name='Wednesday')),
                ('thursday_rotation', models.BooleanField(default=False, verbose_name='Thursday')),
                ('friday_rotation', models.BooleanField(default=False, verbose_name='Friday')),
                ('saturday_rotation', models.BooleanField(default=False, verbose_name='Saturday')),
                ('sunday_rotation', models.BooleanField(default=False, verbose_name='Sunday')),
                ('content_rotation_start_date', models.DateTimeField(blank=True, help_text='The date rotation will begin', null=True)),
                ('content_rotation_end_date', models.DateTimeField(blank=True, help_text='The date rotation will end', null=True)),
                ('enable_next_section', models.BooleanField(default=False, help_text="Activate up next section underneath articles in this section will appear with the heading and subheading of that article. The text will say 'next' in order to make the user feel like it's fresh content.", verbose_name='Activate up next section underneath articles')),
                ('enable_recommended_section', models.BooleanField(default=False, help_text="Underneath the area for 'next articles' recommended articles will appear, with the image + heading + subheading", verbose_name='Activate recommended section underneath articles')),
                ('is_service_aggregator', models.BooleanField(default=False, verbose_name='Service aggregator')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SiteLanguage')),
                ('translated_pages', models.ManyToManyField(blank=True, related_name='_sectionpage_translated_pages_+', to='core.SectionPage')),
            ],
            options={
                'verbose_name': 'Section',
            },
            bases=(molo.core.models.ImportableMixin, molo.core.models.TranslatablePageMixin, 'core.molopage'),
        ),
        migrations.CreateModel(
            name='BannerPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.TextField(blank=True, null=True)),
                ('external_link', models.TextField(blank=True, help_text='External link which a banner will link to. eg https://www.google.co.za/', null=True)),
                ('hide_banner_on_freebasics', models.BooleanField(default=False)),
                ('banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('banner_link_page', models.ForeignKey(blank=True, help_text='Optional page to which the banner will link to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SiteLanguage')),
                ('translated_pages', models.ManyToManyField(blank=True, related_name='_bannerpage_translated_pages_+', to='core.BannerPage')),
            ],
            options={
                'abstract': False,
            },
            bases=(molo.core.models.ImportableMixin, molo.core.models.TranslatablePageMixin, 'core.molopage'),
        ),
        migrations.CreateModel(
            name='ArticlePageRelatedSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('section', models.ForeignKey(blank=True, help_text='Section that this page also belongs too', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_sections', to='core.ArticlePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticlePageRecommendedSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('recommended_article', models.ForeignKey(blank=True, help_text='Recommended articles for this article', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_articles', to='core.ArticlePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticlePageMetaDataTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_articlepagemetadatatag_items', to='taggit.Tag')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='metadata_tagged_items', to='core.ArticlePage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='articlepage',
            name='metadata_tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags. This is not visible to the user.', related_name='metadata_tags', through='core.ArticlePageMetaDataTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='social_media_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='translated_pages',
            field=models.ManyToManyField(blank=True, related_name='_articlepage_translated_pages_+', to='core.ArticlePage'),
        ),
        migrations.CreateModel(
            name='ArticlePageLanguageProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Article View',
                'verbose_name_plural': 'Article View',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.articlepage',),
        ),
    ]
