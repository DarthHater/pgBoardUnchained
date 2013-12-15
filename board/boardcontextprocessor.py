from django.conf import settings

def boardcontextprocessor(request):
	my_dict = {
		'node_host': settings.NODE_HOST,
		'node_port': settings.NODE_PORT,
	}

	return my_dict