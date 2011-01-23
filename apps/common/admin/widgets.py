# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.forms.widgets import Widget
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.utils.translation import ugettext as _
from urlparse import urlparse
from cgi import parse_qs

class AdminImageWidget(Widget):
    def render(self, name, value, attrs=None):
        """
        Renders the picture and value of the picture
        """
        output = u''
        if value and getattr(value, 'extra_thumbnails', None):
            image_url = value.extra_thumbnails['extra'].absolute_url
            output = u'<img src="%s"/>' %  image_url

        return mark_safe(output)

class EditableAdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        """
        Renders the picture and value of the picture
        """
        output = []
        output_from_parent = super(EditableAdminImageWidget, self).render(name, value, attrs)
        if value and hasattr(value, "url"):
            style_params = u'margin-bottom: 10px; max-width: 250px; max-height: 250px;'
            img_output = u'<img src="%s" style="%s"> <br />' %  (value.url, style_params)
            output.append('%s<div style="margin-left:105px;">%s</div>' % \
                (img_output, output_from_parent))
        else:
            output.append(output_from_parent)
        return mark_safe(u''.join(output))

class EditableAdminImageWithThumbnailWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        """
        Renders the picture and value of the picture
        """
        output = []
        output_from_parent = super(EditableAdminImageWithThumbnailWidget, self).render(name, value, attrs)
        if value and hasattr(value, "url"):
            if getattr(value, 'extra_thumbnails', None):
                image_url = value.extra_thumbnails['admin'].absolute_url
                img_output = u'<img src="%s"/ style="margin-bottom: 10px;"> <br />' %  image_url
            else:
                img_output = u''
            output.append('%s<div style="margin-left:105px;">%s</div>' % \
                (img_output, output_from_parent))
        else:
            output.append(output_from_parent)
        return mark_safe(u''.join(output))

class YouTubeAdminVideoWidget(AdminURLFieldWidget):

    width = 640
    height = 385

    @staticmethod
    def get_code_for_url(youtube_url):
        """
        Returns the v parameter from the Youtube's URL video
        """
        if not youtube_url:
            return ''

        qs = urlparse(youtube_url).query
        if qs:
            parsed = parse_qs(qs)
            return parsed.get('v', '')[0]

        return ''

    def render(self, name, value, attrs=None):
        real_tag = super(YouTubeAdminVideoWidget, self).render(name, value, attrs)
        output = []
        if value:
            code = YouTubeAdminVideoWidget.get_code_for_url(value)
            iframe_tag = u'<iframe class="youtube-player" type="text/html" width="%d" height="%d" src="http://www.youtube.com/embed/%s" frameborder="0"></iframe><br/><span style="margin-left: 110px;"></span> ' % (self.width, self.height, code)
            output.append(iframe_tag)
        output.append(real_tag)
        return mark_safe(''.join(output)) 

class SmallYouTubeAdminVideoWidget(YouTubeAdminVideoWidget):

    width = 320
    height = 193
