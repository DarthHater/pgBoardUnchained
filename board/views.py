from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.db.models import Max
from board.models import Forum, Thread, Post
from django.core.context_processors import csrf	
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def list(request):
	""" Get list of threads """
	if request.user.is_authenticated():
		threads = Thread.objects.all().order_by("-last_post_at")
		threads = mk_paginator(request, threads, 50)
		return render_to_response("thread.html", dict(threads=threads, user=request.user))
	else:
		return render_to_response("login.html", add_crsf(request))

@login_required
def thread(request, pk):
	""" Gets posts for a given thread id """
	posts = Post.objects.filter(thread=pk).order_by("created")
	title = Thread.objects.get(pk=pk).title
	return render_to_response("post.html", add_crsf(request, posts=posts, pk=pk, title=title))

def add_crsf(request, ** kwargs):
	d = dict(user=request.user, ** kwargs)
	d.update(csrf(request))
	return d

def mk_paginator(request, items, num_items):
	""" Create and return a paginator """
	paginator = Paginator(items, num_items)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try: 
		items = paginator.page(page)
	except (InvalidPage, EmptyPage):
		items = paginator.page(paginator.num_pages)
	return items

@login_required
def post(request):
	return render_to_response("newthread.html", add_crsf(request))

@login_required
def reply(request, pk):
	""" Reply to a thread """
	p = request.POST
	if p["body"]:
		thread = Thread.objects.get(pk=pk)
		post = Post.objects.create(thread=thread, body=p["body"], creator=request.user)
		thread.last_post_at = post.created
		thread.save()
	return HttpResponseRedirect(reverse("board.views.thread", args=[pk]))

@login_required
def new_thread(request):
	""" Add a new thread """
	p = request.POST
	if p["title"]:
		thread = Thread.objects.create(title=p["title"], creator=request.user)
		post = Post.objects.create(thread=thread, body=p["body"], creator=request.user)
	return HttpResponseRedirect(reverse("board.views.thread", args=[thread.pk]))

def login(request):
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponseRedirect(reverse("board.views.list"))
	else:
		return render_to_response("login.html", add_crsf(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse("board.views.list"))
