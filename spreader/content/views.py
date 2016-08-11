from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from PIL import Image
import urllib.request
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    form = SubmitImage()

    if request.method == 'POST':
        form = SubmitImage(request.POST)
        if form.is_valid():
            try:
                image_file = BytesIO(urllib.request.urlopen(form.cleaned_data['url']).read())
                image = Image.open(image_file)
                image.verify()
            except:
                form.add_error('url', "That link doesn't appear to point to a valid image.")
                return render(request, 'content/index.html', {'form': form})

            ip = ImagePost(url=form.cleaned_data['url'], caption=form.cleaned_data['caption'])
            ip.save()

            p1 = PoolEntry(post=ip)
            p2 = PoolEntry(post=ip)
            p1.save()
            p2.save()

            return HttpResponseRedirect(reverse('permapost', args=[ip.pk]))


    return render(request, 'content/index.html', {'form': form})

def get_post(request):
    if request.GET.get('pool'):
        p = PoolEntry.objects.get(unique_id=request.GET.get('pool'))
        post = p.post
        comments = Comment.objects.filter(post=post).order_by('-time_added')
    else:
        if PoolEntry.objects.order_by('?').exists():
            p = PoolEntry.objects.order_by('?').first()
            post = p.post
            post.views += 1
            post.save()
            comments = Comment.objects.filter(post=post).order_by('-time_added')
        else:
            return HttpResponse('nothing... there is nothing...')

    form = SubmitComment()
    return render(request, 'content/post.html', {'post': post, 'pool': p, 'comments': comments, 'form': form})

def spread_it(request, poolentry_unique_id):
    if PoolEntry.objects.filter(unique_id=poolentry_unique_id).exists():
        p = PoolEntry.objects.get(unique_id=poolentry_unique_id)
        post = p.post
        post.spread += 1
        post.save()
        p.delete()
        p1 = PoolEntry(post=post)
        p2 = PoolEntry(post=post)
        p1.save()
        p2.save()
        return HttpResponseRedirect(reverse('getpost') + '?spread=1')
    else:
        return HttpResponse('no')


def get_next(request, poolentry_unique_id):
    if PoolEntry.objects.filter(unique_id=poolentry_unique_id).exists():
        p = PoolEntry.objects.get(unique_id=poolentry_unique_id)
        p.delete()
        return HttpResponseRedirect(reverse('getpost'))
    else:
        return HttpResponse('no')

def submit_comment(request, poolentry_unique_id):
    if PoolEntry.objects.filter(unique_id=poolentry_unique_id).exists():
        p = PoolEntry.objects.get(unique_id=poolentry_unique_id)
        post = p.post
        form = SubmitComment(request.POST)
        if form.is_valid():
            c = Comment(comment_text=form.cleaned_data['comment'], post=post)
            c.save()
            return HttpResponseRedirect(reverse('getpost') + '?pool=' + poolentry_unique_id)
        else:
            return HttpResponse('???')
    else:
        return HttpResponse('no')


def perma_post(request, post_pk):
    post = ImagePost.objects.get(pk=post_pk)
    comments = Comment.objects.filter(post=post).order_by('-time_added')
    return render(request, 'content/perma_post.html', {'post': post, 'comments': comments})
