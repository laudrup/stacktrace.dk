from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from homepage.models import Post
from homepage.models import Project
from homepage.models import Comment
from homepage.models import CommentForm


def index(request):
    latest_post = Post.objects.order_by('-pub_date')[0]
    return post(request, latest_post.id)

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def post(request, post_id):
    cur_post = Post.objects.get(id = post_id)
    comment_count = Comment.objects.filter(post = post_id).count()
    return render_to_response('post.html', {'cur_post': cur_post, 'comment_count': comment_count},
                              context_instance=RequestContext(request))

def project(request, project_id):
    project = Project.objects.get(id = project_id)
    return render_to_response('project.html', {'project': project},
                              context_instance=RequestContext(request))

def comments(request, post_id):
    cur_post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post = post_id)
    return render_to_response('comments.html', {'cur_post': cur_post, 'comments': comments},
                              context_instance=RequestContext(request))

def comment(request, post_id):
    cur_post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(post = Post(post_id))
            form = CommentForm(request.POST, instance=comment)
            form.save()
            return HttpResponseRedirect('/comments/' + post_id)
    else:
        form = CommentForm()

    # XXX: This is a bit ugly, there has to be a nicer way
    for field in form.fields:
        form.fields[field].widget.attrs = {'class': 'comment-input'}
    form.fields['body'].widget.attrs['rows'] = 10
    form.fields['body'].widget.attrs['cols'] = 40
    return render_to_response('comment.html', {'cur_post': cur_post, 'form': form},
                              context_instance=RequestContext(request))

