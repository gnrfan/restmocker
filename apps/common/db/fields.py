"""
Common DB fields
"""

from django.db.models import CharField
from django.utils.http import int_to_base36
from random import randint

class URLIdField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('max_length', 32)
        super(URLIdField, self).__init__(*args, **kwargs)
        self._min = kwargs.pop('min', 1000000)
        self._max = kwargs.pop('max', 9999999)

    def create_url_id(self, model_class):
        while True:
            value = int_to_base36(randint(self._min, self._max))
            try:
                getargs = {}
                getargs[self.attname] = value
                model_class.objects.get(**getargs)
            except model_class.DoesNotExist:
                return value
    
    def pre_save(self, model, add):
        value = unicode(self.create_url_id(model.__class__))
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
