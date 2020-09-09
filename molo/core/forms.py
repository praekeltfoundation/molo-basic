from django.utils import timezone

from wagtail.admin.forms import WagtailAdminPageForm
from django.utils.translation import ugettext_lazy as _


class ArticlePageForm(WagtailAdminPageForm):

    def clean(self):
        cleaned_data = super(ArticlePageForm, self).clean()

        hero_article = cleaned_data.get("feature_as_hero_article")
        promote_date = cleaned_data.get("promote_date")
        demote_date = cleaned_data.get("demote_date")

        if hero_article:
            if not promote_date:
                self.add_error(
                    "promote_date",
                    _(
                        "Please specify the date and time that you would like "
                        "this article to appear as the Hero Article.")
                )

            if not demote_date:
                self.add_error(
                    "demote_date",
                    _("Please specify the date and time that you would like "
                    "this article to be demoted as the Hero Article.")
                )

            if promote_date and demote_date:
                if promote_date < timezone.now():
                    self.add_error(
                        "promote_date",
                        _("Please select the present date, or a future date.")
                    )

                if demote_date < timezone.now() or demote_date < promote_date:
                    self.add_error(
                        "demote_date",
                        _(
                            "The article cannot be demoted before it has been "
                            "promoted.")
                    )

        return cleaned_data
