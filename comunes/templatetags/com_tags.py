from django import template
from django.utils.translation import ugettext as _

from django.conf import settings
from comunes.utils import thumbnail_exists,create_thumbnail,obj_avatar_url,create_image_thumbnail

register = template.Library()

def image_url(obj,str_imagefield, size=80):
    try:
        img = getattr(obj, str_imagefield)
        if img :
            if not thumbnail_exists(obj,size,str_imagefield):
                create_thumbnail(obj,size,str_imagefield)
            return obj_avatar_url(obj,size,str_imagefield)
        elif str_imagefield != "avatar" :
            return ""
    except Exception:
        pass
    return settings.AVATAR_DEFAULT_URL
register.simple_tag(image_url)



def photo_image_url(obj,str_imagefield, size = 300):
    try:
        img = getattr(obj, str_imagefield)
        if img :
            if not thumbnail_exists(obj,size,str_imagefield):
                create_image_thumbnail(obj,size,str_imagefield)
            return obj_avatar_url(obj,size,str_imagefield)
        elif str_imagefield != "avatar" :
            return ""
    except Exception:
        pass
    return settings.AVATAR_DEFAULT_URL
register.simple_tag(photo_image_url)

def image(obj,str_imagefield, size=80):
    try:
        #alt = unicode(user) Poner un alt con el name del object
        alt = _("Default Avatar")
        url = image_url(obj, str_imagefield,size)
    except Exception:
        url = settings.AVATAR_DEFAULT_URL
        alt = _("Default Avatar")
    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (url, alt,
        size, size)
register.simple_tag(image)

def image_or_default(obj,str_imagefield, size=80):
    try:
        img = getattr(obj, str_imagefield)
        if img :
            if not thumbnail_exists(obj,size,str_imagefield):
                create_thumbnail(obj,size,str_imagefield)
            return obj_avatar_url(obj,size,str_imagefield)
        else  :
            return "/media/images/default/default_avatar.jpg"
    except Exception:
        pass
    return settings.AVATAR_DEFAULT_URL
register.simple_tag(image_or_default)
