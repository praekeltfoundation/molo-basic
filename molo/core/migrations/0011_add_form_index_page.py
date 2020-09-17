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
        ('core', '0010_formindexpage_formsubmission'),
    ]

    operations = [
        migrations.RunPython(create_form_index),
    ]
