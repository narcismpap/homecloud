from django.utils.translation import ugettext as _
import base


class ActorHelper(base.BaseUI):

    def __init__(self, request):
        base.BaseUI.__init__(self, request)

    def page_actor_details(self, actor):
        self.current_page = base.PAGE_ACTOR_SINGLE
        self.local_variables["Actor"] = actor
        self.local_variables["Title"] = _("Actori > %s") % actor.name

        return self.render("pages/actor_single.html")