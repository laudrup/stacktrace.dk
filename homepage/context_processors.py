import urllib, hashlib
from django.conf import settings
from homepage.models import Post
from homepage.models import Project

def base(request):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(settings.GRAVATAR_MAIL.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'s':str(48)})
    posts = Post.objects.order_by('-pub_date')
    projects = Project.objects.all()
    return {'posts': posts, 'projects': projects, 'gravatar_url': gravatar_url}
