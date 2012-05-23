#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
import inspect

class MetaClass(type):
    def __new__(self, classname, classbases, classdict):
        try:
            frame = inspect.currentframe()
            frame = frame.f_back
            if frame.f_locals.has_key(classname):
                old_class = frame.f_locals.get(classname)
                for name,func in classdict.items():
                    if inspect.isfunction(func):
                        setattr(old_class, name, func)
                return old_class
            return type.__new__(self, classname, classbases, classdict)
        finally:
            del frame

class MetaObject(object):
    __metaclass__ = MetaClass

class User(MetaObject):
    def get_user_role(self):
        return self.user_info.userRole

    def get_user_nickname(self):
        return  self.user_info.nickname