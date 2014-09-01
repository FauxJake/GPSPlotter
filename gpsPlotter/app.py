from wsgiref.simple_server import make_server
import urlparse, os
import json as simplejson
import jinja2

dispatch = {
	'/' : 'index',
	'/results' : 'results'
}

headers = [('Content-Type', 'text/html')]

class gpsPlotterApp(object):
	def __call__(self, environ, start_response):
		path = environ['PATH_INFO']

		fn_name = dispatch.get(path, 'error')
		fn = getattr(self, fn_name, None)

		if fn is None:
			start_response("404 Not Found", headers)
			return ["No path %s found % path"]

		return fn(environ, start_response)

	def index(self, environ, start_response):
		data = index()
		start_response('200 OK', headers)
		return data 

# HELPER FUNCTIONS
def JinjaLoader(filename,vars):
	# this sets up jinja2 to load templates from the 'templates' directory
	basepath = os.path.dirname(__file__)
	filepath = os.path.abspath(os.path.join(basepath,'JinjaTemplates'))
	#print filepath
	loader = jinja2.FileSystemLoader(filepath)
	#print loader.list_templates()
	env = jinja2.Environment(loader=loader)
	# pick up a filename to render
	template = env.get_template(filename)
	x = template.render(vars).encode('ascii','ignore')
	return x

# HTML TEMPLATING
def index():
	vars = dict()
	return JinjaLoader('index.html', vars)