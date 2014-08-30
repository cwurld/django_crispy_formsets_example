# Inspired by http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/

from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.views.generic import ListView
from django.core.urlresolvers import reverse, reverse_lazy

from braces.views import SetHeadlineMixin

import models
import forms


# noinspection PyAttributeOutsideInit
class ParentMixin(SetHeadlineMixin):
    model = models.Parent
    form_class = forms.ParentForm
    child_model = models.Child
    template_name = 'example/crispy_formsets.html'
    success_url = reverse_lazy('list_parents')

    def setup_get_or_post(self, post_data=None):
        form_class = self.get_form_class()
        parent_form = self.get_form(form_class)

        # Child forms
        child_form = forms.gen_child_form(self.object)
        formset_class = inlineformset_factory(self.model, self.child_model, form=child_form, extra=1)
        child_formset = formset_class(instance=self.object, data=post_data)
        return parent_form, child_formset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        parent_form, child_formset = self.setup_get_or_post()
        return self.render_to_response(self.get_context_data(parent_form=parent_form,
                                                             child_formset=child_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        parent_form, child_formset = self.setup_get_or_post(self.request.POST)

        # If you call the is_valid method as part of a chain of and statements in the "if" below, then all the
        # forms after the first invalid form will not be cleaned. Thus we call each form validator in a statement
        # its self.
        parent_form_is_valid = parent_form.is_valid()
        print 'parent valid', parent_form_is_valid
        child_formset_is_valid = child_formset.is_valid()
        print 'child formset valid', child_formset_is_valid

        if parent_form_is_valid and child_formset_is_valid:
            return self.form_valid(parent_form, child_formset)
        else:
            return self.form_invalid(parent_form, child_formset)

    def form_valid(self, parent_form, child_formset):
        self.object = parent_form.save()
        child_formset.instance = self.object
        child_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, parent_form, child_formset):
        return self.render_to_response(self.get_context_data(parent_form=parent_form,
                                                             child_formset=child_formset))


class ParentCreate(ParentMixin, CreateView):
    headline = 'Create Parent and Children'

    def get_object(self):
        return None

class ParentUpdate(ParentMixin, UpdateView):
    headline = 'Update Parent and Children'

class ParentList(ListView):
    model = models.Parent

