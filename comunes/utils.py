import os
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.auth import login

#from account.signals import user_logged_in
try:
    from PIL import Image
except ImportError:
    import Image

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
from django.template.defaultfilters import slugify
from os.path import splitext

def get_upload_path(instance, filename):
    import datetime
    import hashlib
    now = datetime.datetime.now()
    return type(instance).__name__+'_image/'+hashlib.md5(str(now)).hexdigest()+'.jpg'


def get_upload_path_file(instance, filename):
    import datetime
    import hashlib
    now = datetime.datetime.now()
    extension=filename.split(".")[-1]
    return type(instance).__name__+'_file/'+slugify(splitext(filename)[0])+'.'+extension

def avatar_name(obj, size,str_name):
    path=getattr(obj, str_name).name
    name=path[path.index('/')+1:]
    ruta=type(obj).__name__+'_image/'+slugify(obj.id)
    return os.path.join(settings.MEDIA_ROOT, ruta,
            'resized', str(size), name)
    
def thumbnail_exists(obj, size,str_name):
        return getattr(obj, str_name).storage.exists(avatar_name(obj,size,str_name))
    
def create_thumbnail(obj, size,str_name):
        img=getattr(obj, str_name)
        try:
            orig = img.storage.open(img.name, 'rb').read()
            image = Image.open(StringIO(orig))
        except IOError:
            return # What should we do here?  Render a "sorry, didn't work" img?
        (w, h) = image.size
        if w != size or h != size:
            if w > h:
                diff = (w - h) / 2
                image = image.crop((diff, 0, w - diff, h))
            else:
                diff = (h - w) / 2
                image = image.crop((0, diff, w, h - diff))
            image = image.resize((size, size), Image.ANTIALIAS)
            if image.mode != "RGB":
                image = image.convert("RGB")
            thumb = StringIO()
            image.save(thumb, "JPEG")
            thumb_file = ContentFile(thumb.getvalue())
        else:
            thumb_file = ContentFile(orig)
        thumb = img.storage.save(avatar_name(obj,size,str_name), thumb_file)

def create_image_thumbnail(obj, size,str_name):
        img=getattr(obj, str_name)
        try:
            orig = img.storage.open(img.name, 'rb').read()
            image = Image.open(StringIO(orig))
        except IOError:
            return # What should we do here?  Render a "sorry, didn't work" img?
        (w, h) = image.size
        if w > size or h > 300:
            if w > h:
                ancho = size
                alto = (size*h)/w
            else:
                ancho = (300*w)/h
                alto = 300
            image = image.resize((ancho, alto), Image.ANTIALIAS)
            
            if image.mode != "RGB":
                image = image.convert("RGB")
            thumb = StringIO()
            image.save(thumb, "JPEG")
            thumb_file = ContentFile(thumb.getvalue())
        else:
            thumb_file = ContentFile(orig)
        thumb = img.storage.save(avatar_name(obj,size,str_name), thumb_file)

def obj_avatar_url(obj, size,str_name):
    path=getattr(obj, str_name).name
    name=path[path.index('/')+1:]
    ruta=type(obj).__name__+'_image/'+slugify(obj.id)
    return os.path.join(settings.MEDIA_URL, ruta,
            'resized', str(size), name)





LOGIN_REDIRECT_URLNAME = getattr(settings, "LOGIN_REDIRECT_URLNAME", "")


def get_default_redirect(request, redirect_field_name="next",
        login_redirect_urlname=LOGIN_REDIRECT_URLNAME, session_key_value="redirect_to"):
    """
    Returns the URL to be used in login procedures by looking at different
    values in the following order:
    
    - a REQUEST value, GET or POST, named "next" by default.
    - LOGIN_REDIRECT_URL - the URL in the setting
    - LOGIN_REDIRECT_URLNAME - the name of a URLconf entry in the settings
    """
    if login_redirect_urlname:
        default_redirect_to = reverse(login_redirect_urlname)
    else:
        default_redirect_to = settings.LOGIN_REDIRECT_URL
    redirect_to = request.REQUEST.get(redirect_field_name)
    if not redirect_to:
        # try the session if available
        if hasattr(request, "session"):
            redirect_to = request.session.get(session_key_value)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = default_redirect_to
    return redirect_to


#def perform_login(request, user):
#    user_logged_in.send(sender=user.__class__, request=request, user=user)
#    login(request, user)