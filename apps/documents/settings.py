# -*- coding: utf-8 -*-

from django.conf import settings
from documents import constants

REALM_PAGINATE_BY = getattr(settings,
    'REALM_PAGINATE_BY',
    constants.REALM_PAGINATE_BY)

DOCUMENT_PAGINATE_BY = getattr(settings,
    'DOCUMENT_PAGINATE_BY',
    constants.DOCUMENT_PAGINATE_BY)
