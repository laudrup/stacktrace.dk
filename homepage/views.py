from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from homepage.models import Post
from homepage.models import Project
from homepage.models import Comment
from homepage.models import CommentForm
from homepage.models import Gallery

def index(request):
    latest_post = Post.objects.order_by('-pub_date')[0]
    return post(request, latest_post.id)

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def post(request, post_id):
    cur_post = Post.objects.get(id = post_id)
    comment_count = Comment.objects.filter(post = post_id, approved=True).count()
    return render_to_response('post.html', {'cur_post': cur_post, 'comment_count': comment_count},
                              context_instance=RequestContext(request))

def project(request, project_id):
    project = Project.objects.get(id = project_id)
    return render_to_response('project.html', {'project': project},
                              context_instance=RequestContext(request))

def comments(request, post_id):
    cur_post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post = post_id, approved=True)
    return render_to_response('comments.html', {'cur_post': cur_post, 'comments': comments},
                              context_instance=RequestContext(request))

def comment(request, post_id):
    cur_post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if len(request.POST['subject']) != 0:
                return HttpResponse('Subject field should remain empty')
            comment = Comment(post = Post(post_id))
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

def photos(request, gallery_id=None):
    if gallery_id:
        gallery = Gallery.objects.get(title_slug = gallery_id)
        title = gallery.title
        objects = gallery.photos.all()
    else:
        objects = Gallery.objects.all()
        title = 'None'
    return render_to_response('photos.html', {'objects': objects},
                              context_instance=RequestContext(request))
