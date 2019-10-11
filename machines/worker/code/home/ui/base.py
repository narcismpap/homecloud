from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
import string, random
from home.models import Movie

PAGE_MOVIES = 10
PAGE_MOVIE_SINGLE = 15
PAGE_ACTORS = 20
PAGE_ACTOR_SINGLE = 25


class BaseUI:

    def __init__(self, request):
        self.request = request
        self.current_page = 0
        self.local_variables = {}

    def template_variables(self, variables):
        variables["ApplicationVesion"] = "1.0"
        variables["MovieCount"] = Movie.objects.count()
        variables["ShowCount"] = "N/A"

        if self.request.user.is_authenticated():
            variables["CurrentUser"] = self.request.user
        else:
            variables["CurrentUser"] = None

        if self.local_variables:
            for s, v in self.local_variables.iteritems():
                variables[s] = v

        return variables

    def render(self, template, variables=None):
        variables = self.template_variables(variables if variables else {})
        return render_to_response(template, variables, context_instance=RequestContext(self.request))

    def permission_error(self):
        raise PermissionDenied

    def not_found_error(self):
        raise Http404

    def get_page_url(self, name):
        return reverse(name)

    def get_page_url_parameters(self, name, parameters):
        return reverse(name, args=parameters)

    def redirect_custom(self, url):
        return redirect(url)

    def random_string(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))