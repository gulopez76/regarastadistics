# -*- coding: utf-8 -*-
from django.template.defaultfilters import stringfilter
from django import template
from datacubes.models import userprofile
from django.contrib.auth.models import User
from django.conf import settings

register = template.Library()

@register.filter
def photoid(pid):
    pid = userprofile.objects.only('user_id', 'photo').all()
    return pid 

@register.filter
def getindex(vdict, key):
	return vdict.get(key,'')

@register.filter
def get(vdict, key):
	return vdict.get(key,'')

@register.filter
def lendict(vdict, count):
	count = len(vdict)
	return count

@register.filter
@stringfilter
def int_to_string(value):
    return value

@register.filter
def str_to_int(value):
    return int(value)

@register.filter
def replace_to(value):
    return value.replace(".",",")
