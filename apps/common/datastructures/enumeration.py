# -*- coding: utf-8 -*-
    # Taken fron http://djangosnippets.org/snippets/1647/
# Author: Dmitri Patrakov <traditio@gmail.com>

class Enumeration(object):
    """
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.

    Example:
        MY_ENUM = Enumeration([
            (100, 'MY_NAME', 'My verbose name'),
            (200, 'MY_AGE', 'My verbose age'),
        ])
        assert MY_ENUM.MY_AGE == 100
        assert MY_ENUM[1] == (200, 'My verbose age')
    """

    def __init__(self, enum_list):
        self.enum_keys = [(item[0], item[1]) for item in enum_list]
        self.enum_list = [(item[0], item[2]) for item in enum_list]
        self.enum_dict = {}
        for item in enum_list:
            self.enum_dict[item[1]] = item[0]
            
    def __contains__(self, v):
        return (v in self.enum_list)

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, v):
        if isinstance(v, basestring):
            return self.enum_dict[v]
        elif isinstance(v, int):
            return self.enum_list[v]

    def __getattr__(self, name):
        return self.enum_dict[name]

    def insert(self, pos, item):
        self.enum_keys.insert(pos, (item[0], item[1]))
        self.enum_list.insert(pos, (item[0], item[2]))
        self.enum_dict[item[1]] = item[0]
        
    def append(self, item):
        self.enum_keys.append((item[0], item[1]))
        self.enum_list.append((item[0], item[2]))
        self.enum_dict[item[1]] = item[0]

    def get_string(self, v):
        string_dict = dict(self.enum_list)
        try:
            if isinstance(v, basestring):
                return string_dict[self.enum_dict[v]]
            elif isinstance(v, int):
                return string_dict[v]
        except KeyError:
            return None

    def get_key(self, v):
        key_dict = dict(self.enum_keys)
        return key_dict.get(v)

    def get_value(self, v):
        return self.enum_dict.get(v)

    def __iter__(self):
        return self.enum_list.__iter__()
                                                                               
    def values(self):                                                           
        return [item[0] for item in self.enum_list]                             
                                                                                
    def keys(self):                                                             
        return [item[1] for item in self.enum_keys]   

    def has_key(self, key):
        return key in self.keys()

    def has_value(self, value):
        return value in self.values()

    def get_tuple(self):
        result = []
        for k,v in self.enum_keys:
            result.append((k, v, self.get_string(k),) )
        return tuple(result)

    def clone(self):
        return Enumeration(self.get_tuple())

