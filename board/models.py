from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.urlresolvers import reverse
from string import join

import bbcode
import re

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
		parser = bbcode.Parser()
		""" Seems like the following line could be done in a module where I define more overrides? Sloppy but I'm a python n00bie """
		parser.add_simple_formatter('img', '<img class="img-responsive" src=''%(value)s'' />', replace_links=False)
		parser.add_formatter('youtube', render_youtube, replace_links=False)
		parser.add_formatter('bandcamp', render_bandcamp, replace_links=False)
		parser.add_formatter('vimeo', render_vimeo, replace_links=False)
		parser.add_formatter('soundcloud', render_soundcloud, replace_links=False)
		return parser.format(self.body)

	def short(self):
		return u"%s - %s\n%s" % (self.creator, self.thread.title, self.created.strftime("%b %d, %I:%M %p"))

	def thread_id(self):
		return self.thread__pk

	short.allow_tags = True

# bbcode parsers

def render_soundcloud(tag_name, value, options, parent, context):
	track_path_regex = re.compile('soundcloud.com\/(?P<track_path>.+)')
	r = track_path_regex.search(value)
	if r:
		return	"""<iframe
				src="http://w.soundcloud.com/player/?url=http://api.soundcloud.com/%(track_path)s"></iframe>""" % r.groupdict()
	return ''

def render_vimeo(tag_name, value, options, parent, context):
	video_id_regex = re.compile("vimeo.com\/(?P<video_id>[0-9+])", re.I)
	r = video_id_regex.search(value)
	if r:
		return """
		<iframe src="http://player.vimeo.com/video/%(video_id)s"
		width="400" height="400" frameborder="0"
		webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
		""" % r.groupdict()
	return ''

def render_bandcamp(tag_name, value, options, parent, context):
	album_id_regex = re.compile("(?P<track_or_album>[a-z]+)=(?P<id>[0-9]+)", re.I)
	r = album_id_regex.search(value)
	print(r.groupdict())
	if r:
		return	"""<iframe
				src='http://bandcamp.com/EmbeddedPlayer/%(track_or_album)s=%(id)s>'
				</iframe>""" % r.groupdict()
	return ''

def render_youtube(tag_name, value, options, parent, context):
	videoid = youtube_url_validation(value)
	return '<div class="flex-video widescreen"><iframe id="ytplayer" type="text/html" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen=""></iframe></div>' % (videoid)

def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)
    return youtube_regex_match