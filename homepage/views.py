from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.static import serve
from homepage.models import *

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

def galleries(request):
    galleries = get_list_or_404(Gallery)
    paginator = Paginator(galleries, 8)
    page = request.GET.get('page')
    if not page:
        galleries = paginator.page(1)
    else:
        try:
            galleries = paginator.page(page)
        except PageNotAnInteger:
            galleries = paginator.page(1)
        except EmptyPage:
            galleries = paginator.page(paginator.num_pages)
    return render_to_response('galleries.html', {'galleries': galleries},
                              context_instance=RequestContext(request))

def photos(request, gallery_id):
    gallery = get_object_or_404(Gallery, slug = gallery_id)
    title = gallery.title
    photos = gallery.photo_set.all()
    paginator = Paginator(photos, 8)
    page = request.GET.get('page')
    if not page:
        photos = paginator.page(1)
    else:
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)
    return render_to_response('photos.html', {'photos': photos, 'title': title},
                              context_instance=RequestContext(request))

def secure(request):
    if request.path.startswith(settings.MEDIA_URL):
        path = request.path[len(settings.MEDIA_URL):]
    else:
        path = request.path
    return serve(request, path, document_root=settings.MEDIA_ROOT)
