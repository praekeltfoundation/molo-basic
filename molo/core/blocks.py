from django.utils.safestring import mark_safe
from markdown import markdown

from wagtail.core import blocks
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class MarkDownBlock(blocks.TextBlock):
    """ MarkDown Block """

    class Meta:
        icon = 'code'

    def render_basic(self, value, context=None):
        md = markdown(
            value,
            extensions=[
                'markdown.extensions.fenced_code',
                'codehilite',
            ],
        )
        return mark_safe(md)


class SocialMediaLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    link = blocks.CharBlock(required=True)
    image = ImageChooserBlock()
