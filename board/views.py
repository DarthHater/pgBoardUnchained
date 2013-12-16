from django.shortcuts import render_to_response, redirect, render
from django.core.urlresolvers import reverse
from django.db.models import Max
from board.models import Forum, Thread, Post, User
from django.core.context_processors import csrf	
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import formats
from datetime import datetime
from django.conf import settings

import json
import redis
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
	response_dict = RequestContext(request)
	""" Gets posts for a given thread id """
	posts = Post.objects.filter(thread=pk).order_by("created")
	title = Thread.objects.get(pk=pk).title
	return render_to_response("post.html", add_crsf(request, posts=posts, pk=pk, title=title, threadpk=pk), response_dict)

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

@csrf_exempt
def thread_api(request):
	try:
		# Get User
		session = Session.objects.get(session_key=request.POST.get('sessionid'))
		user_id = session.get_decoded().get('_auth_user_id')
		user = User.objects.get(id=user_id)

		# Create post, I was getting thread because I've yet to figure out how to pass it in to this
		thread = Thread.objects.get(pk=request.POST.get('thread'))
		post = Post.objects.create(thread=thread, body=request.POST.get('comment'), creator=user)
		thread.last_post_at = post.created
		thread.save()

		# Connect to redis and add post to thread channel, need to change it to add to the thread specific channel
		post_dict = {'user': user.username,
			'created': str(formats.date_format(post.created, "DATETIME_FORMAT")),
			'comment': request.POST.get('comment')
			}

		r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASSWORD)
		
		r.publish('thread_' + str(thread.pk), json.dumps(post_dict))

		return HttpResponse("Everything worked :)")
	except Exception, e:
		return HttpResponseServerError(str(e))

@login_required
def test(request, pk):
	thread = Thread.objects.get(pk=pk)
	posts = Post.objects.filter(thread=thread).order_by("created")
	return render_to_response("threadpost.html", dict(posts=posts))
