from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    from homepage.models import Post
    cur_post = Post.objects.order_by('-pub_date')[0]
    return render_to_response('post.html', {'cur_post': cur_post},
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def post(request, post_id):
    from homepage.models import Post
    cur_post = Post.objects.get(id = post_id)
    return render_to_response('post.html', {'cur_post': cur_post},
                              context_instance=RequestContext(request))
