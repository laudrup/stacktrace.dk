from homepage.models import StackTrace
from homepage.models import Post

def base(request):
    posts = Post.objects.order_by('-pub_date')
    stacktrace = StackTrace.objects.all()
    return {'stacktrace': stacktrace, 'posts': posts}
