import bbcode, re

def render_bbcode(text):
		parser = bbcode.Parser()
		""" Seems like the following line could be done in a module where I define more overrides? Sloppy but I'm a python n00bie """
		parser.add_simple_formatter('img', '<img class="img-responsive" src=''%(value)s'' />', replace_links=False)
		parser.add_formatter('youtube', render_youtube, replace_links=False)
		parser.add_formatter('bandcamp', render_bandcamp, replace_links=False)
		parser.add_formatter('vimeo', render_vimeo, replace_links=False)
		parser.add_formatter('soundcloud', render_soundcloud, replace_links=False)
		return parser.format(text)

def render_soundcloud(tag_name, value, options, parent, context):
	track_path_regex = re.compile('soundcloud.com\/(?P<track_path>.+)')
	r = track_path_regex.search(value)
	if r:
		return	"""<iframe
			src="http://w.soundcloud.com/player/
			?url=http://api.soundcloud.com/%(track_path)s"
			</iframe>
			""" % r.groupdict()
	return ''

def render_vimeo(tag_name, value, options, parent, context):
	video_id_regex = re.compile("vimeo.com\/(?P<video_id>[0-9]+)", re.I)
	r = video_id_regex.search(value)
	if r:
		return """<iframe
		src="http://player.vimeo.com/video/%(video_id)s"
		width="400" height="400" frameborder="0"
		webkitallowfullscreen mozallowfullscreen allowfullscreen>
		</iframe>
		""" % r.groupdict()
	return ''

def render_bandcamp(tag_name, value, options, parent, context):
	album_id_regex = re.compile("(?P<track_or_album>[a-z]+)=(?P<id>[0-9]+)", re.I)
	r = album_id_regex.search(value)
	if r:
		return	"""<iframe
			src='http://bandcamp.com/EmbeddedPlayer/%(track_or_album)s=%(id)s'
			</iframe>
			""" % r.groupdict()
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