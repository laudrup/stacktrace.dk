from homepage.models import Post
from homepage.models import Project
from django.conf import settings

def base(request):
    posts = Post.objects.order_by('-pub_date')
    projects = Project.objects.all()
    return {'posts': posts, 'projects': projects, 'STATIC_URL': settings.STATIC_URL}
