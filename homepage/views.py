from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from homepage.models import *
import os

def index(request):
    latest_post = Post.objects.order_by('-pub_date')[0]
    return post(request, latest_post.slug)

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def post(request, post_id):
    cur_post = get_object_or_404(Post, slug = post_id)
    comment_count = Comment.objects.filter(post = cur_post.id, approved=True).count()
    return render_to_response('post.html', {'cur_post': cur_post, 'comment_count': comment_count},
                              context_instance=RequestContext(request))

def project(request, project_id):
    project = get_object_or_404(Project, slug = project_id)
    return render_to_response('project.html', {'project': project},
                              context_instance=RequestContext(request))

def comments(request, post_id):
    cur_post = get_object_or_404(Post, slug = post_id)
    comments = Comment.objects.filter(post = cur_post.id, approved=True)
    return render_to_response('comments.html', {'cur_post': cur_post, 'comments': comments},
                              context_instance=RequestContext(request))

def comment(request, post_id):
    cur_post = get_object_or_404(Post, slug = post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if len(request.POST['subject']) != 0:
                return HttpResponse('Subject field should remain empty')
            comment = Comment(post = Post(cur_post.id))
            form = CommentForm(request.POST, instance=comment)
            form.save()
            admin_mails = [admin[1] for admin in settings.ADMINS]
            mail_subject = 'A comment has been post by {0}'.format(form.cleaned_data['author'])
            send_mail(mail_subject, form.cleaned_data['body'], form.cleaned_data['email'], admin_mails)
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

@login_required
def photos(request, gallery_id = None):
    if gallery_id is not None:
        gallery = get_object_or_404(Gallery, slug = gallery_id)
        objects = gallery.photo_set.all()
    else:
        objects = get_list_or_404(Gallery)
    paginator = Paginator(objects, 8)
    page = request.GET.get('page')
    if not page:
        objects = paginator.page(1)
    else:
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
    if gallery_id is not None:
        return render_to_response('photos.html', {'objects': objects, 'gallery': gallery},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('galleries.html', {'objects': objects},
                                  context_instance=RequestContext(request))

def get_absolute_filename(path):
    if not path or '..' in path.split(os.path.sep):
        raise PermissionDenied
    return os.path.join(settings.MEDIA_ROOT, path)

@login_required
def media(request, path):
    abs_filename = get_absolute_filename(path)
    response = HttpResponse()
    del response['content-type']
    response['X-Sendfile'] = abs_filename
    return response
