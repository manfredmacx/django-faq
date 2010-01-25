"""
Home base for all application enums.
"""
from django.utils.translation import ugettext_lazy as _

STATUS_HEADER = 2
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0

QUESTION_STATUS_CHOICES = (
    (STATUS_ACTIVE, _(u'Active')),
    (STATUS_INACTIVE, _(u'Inactive')),
    (STATUS_HEADER, _(u'Group Header'))
)
