from django.shortcuts import render_to_response

from homepage.models import StackTrace
from homepage.models import Post

def index(request):
    stacktrace = StackTrace.objects.all()
    posts = Post.objects.order_by('pub_date').reverse()
    return render_to_response('index.html', {'stacktrace': stacktrace, 'posts': posts})

def about(request):
    stacktrace = StackTrace.objects.all()
    posts = Post.objects.order_by('pub_date').reverse()
    return render_to_response('about.html', {'stacktrace': stacktrace, 'posts': posts})

def contact(request):
    stacktrace = StackTrace.objects.all()
    posts = Post.objects.order_by('pub_date').reverse()
    return render_to_response('contact.html', {'stacktrace': stacktrace, 'posts': posts})

def post(request, post_id):
    stacktrace = StackTrace.objects.all()
    posts = Post.objects.order_by('pub_date').reverse()
    cur_post = Post.objects.get(id = post_id)
    return render_to_response('post.html', {'stacktrace': stacktrace, 'posts': posts, 'cur_post': cur_post})
