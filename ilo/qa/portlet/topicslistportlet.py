from five import grok
from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone import api


grok.templatedir('templates')

class IContentNavigation(IPortletDataProvider):
    
    portlet_title = schema.TextLine(
            title = u"Add Question Button Label",
            required=False,
        )


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self, portlet_title=None):
        self.portlet_title = portlet_title
       
       
    @property
    def title(self):
        return "Add Topics List Portlet"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/topicslistportlet.pt')
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
        
    def contents(self):
        return self.data

    def topics(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        # import pdb; pdb.set_trace()
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.topic', sort_on='Date',sort_order='reverse')
        return brains

    def roles(self):
        current = api.user.get_current()
        roles = api.user.get_roles(username=str(current))
        return any((True for x in roles if x in ['Reviewer', 'Administrator', 'Manager'] ))

    def review_state(self, review_state = None):
        if '_' in review_state:
            return review_state.replace('_', ' ')
        else:
            return review_state
    
class AddForm(base.AddForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Add Topics List Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Edit Topics List Portlet"
    description = ''
