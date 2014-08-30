__author__ = 'Chuck Martin'

from django import forms

from crispy_forms.layout import Layout, Submit, Field, Div, HTML
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineField

import models


class ParentForm(forms.ModelForm):
    class Meta:
        model = models.Parent

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Parent Name'

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.form_tag = False
        self.helper.layout = Layout('name', Field('description', rows="2"))


def gen_child_form(parent_instance):
    """
    There is no easy way to get extra parameters into the child form. So we will use a closure to do that.

    This function returns a form class that knows about the parent instance.
    """
    class ChildForm(forms.ModelForm):
        class Meta:
            model = models.Child
            fields = ('name', )

            # Would like to use crispy here, but does not do what I want when the child forms are part of the
            # parent form
            widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': 'add child name'})}

        def __init__(self, *args, **kwargs):
            super(ChildForm, self).__init__(*args, **kwargs)
            self.parent_instance = parent_instance  # from outer scope

            # Do stuff,like set choices or defaults, etc...

        #
        # def has_changed(self, *args, **kwargs):
        #     """
        #     If you include blank child forms on your page, django needs to decide whether or not to save them. The
        #     default has_changed method is to save any form that has changed from the initial values.
        #
        #     In some cases you might want to over-ride that. Here is a stub. Look at the django source code for
        #     details on how to write your code.
        #     """
        #     # TODO: change or delete this method
        #     return super(ChildForm, self).has_changed(*args, **kwargs)

        # def clean_name(self):
        #     name = self.cleaned_data['name']
        #     if name == 'Joe':
        #         raise forms.ValidationError('No children named Joe')
        #     return name

    return ChildForm


class ChildFormHelper(FormHelper):
    # See: http://stackoverflow.com/questions/18474260/using-html-in-crispy-forms-formset
    pass

