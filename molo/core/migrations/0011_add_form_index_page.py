from django.db import migrations


def create_form_index(apps, schema_editor):
    from molo.core.models import FormIndexPage, Main
    main = Main.objects.all().first()

    if main:
        form_index = FormIndexPage(title='Forms', slug='form-pages')
        main.add_child(instance=form_index)
        form_index.save_revision().publish()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_formfield_formindexpage_formpage_formsubmission'),
    ]

    operations = [
        migrations.RunPython(create_form_index),
    ]
