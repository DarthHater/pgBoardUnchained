from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.urlresolvers import reverse
from string import join

import bbcode
import re

from board.modules.parsers import render_bbcode

# Created my models here lulz
class Forum(models.Model):
	title = models.CharField(max_length=60)

	def __unicode__(self):
		return self.title

	def num_posts(self):
		return sum([t.num_posts() for t in self.thread_set.all()])

	def last_post(self):
		if self.thread_set.count():
			last = None
			for t in self.thread_set.all():
				l = t.last_post()
				if l:
					if not last: last = l
				elif l.created > last.created: last = l
			return last

	def get_absolute_url(self):
		return reverse('board.views.list')

class Thread(models.Model):
	title = models.CharField(max_length=120)
	created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User, blank=True, null=True)
	last_post_at = models.DateTimeField(auto_now_add=True, null=True)

	def __unicode__(self):
		return unicode(self.creator) + " - " + self.title

	def num_posts(self):
		return self.post_set.count()

	def num_replies(self):
		return self.post_set.count() - 1

	def last_post(self):
		if self.post_set.count():
			return self.post_set.order_by("-created")[0].created

	def last_poster(self):
		if self.post_set.count():
			return self.post_set.order_by("-created")[0].creator 

	def get_absolute_url(self):
		return reverse('board.views.thread', args=[self.pk,])

class Post(models.Model):
	created  = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User, blank=True, null=True)
	thread = models.ForeignKey(Thread)
	body =  models.TextField()

	def __unicode__(self):
		return u"%s - %s" % (self.creator, self.thread)

	def bodybbcode(self):
		return render_bbcode(self.body)

	def short(self):
		return u"%s - %s\n%s" % (self.creator, self.thread.title, self.created.strftime("%b %d, %I:%M %p"))

	def thread_id(self):
		return self.thread__pk

	short.allow_tags = True

class UserProfile(models.Model):
	posts = models.IntegerField(default=0)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return unicode(self.user)

def create_user_profile(sender, **kwargs):
	""" Creates a User Profile on User creation """
	u = kwargs["instance"]
	if not UserProfile.objects.filter(user=u):
		UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)