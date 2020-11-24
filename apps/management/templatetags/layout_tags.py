# from django import template
#
# from apps.management.models import Announcement
#
# register = template.Library()
#
#
# @register.simple_tag()
# def messages():
#     announcements = Announcement.objects.filter(status=1)
#
#     return announcements