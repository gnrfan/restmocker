# -*- coding: utf-8 -*-

from django.forms.widgets import Select

class SelectWithEmptyLabel(Select):
    def __init__(self, attrs=None, choices=(), empty_label='---------', *args, **kwargs):
        self.empty_label = empty_label
        super(SelectWithEmptyLabel,self).__init__(attrs=attrs, choices=choices, *args, **kwargs)
        self.choices.insert(0, ('', self.empty_label))
