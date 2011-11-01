from homepage.models import Post
from homepage.models import Project

def base(request):
    posts = Post.objects.order_by('-pub_date')
    projects = Project.objects.all()
    return {'posts': posts, 'projects': projects}
