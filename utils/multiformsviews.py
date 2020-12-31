"""View for proccessing multiple forms."""
import re
from django.views.generic.base import TemplateResponseMixin
from django.http import HttpResponseForbidden
from django.views.generic.edit import ProcessFormView, ContextMixin
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured


class MultiFormsMixin(ContextMixin):
    """
    Mixin to similiar to FormMixin but proccess multiple forms.

    It will work with a single form,
    but probably it would be more straightforward to use
    bult-in django FormMixin.
    """

    form_classes = {}
    prefixes = {}
    success_urls = {}
    initials = {}

    def get_form_classes(self, form_names=None):
        """
        Return the form class names defined in the view.

        If form_names is supplied it will return classes for only those
        form names.
        """
        if form_names is not None:
            form_classes = {}
            for form_name in form_names:
                form_classes[form_name] = self.form_classes.get(form_name)
            return form_classes
        return self.form_classes

    def get_form_class(self, form_name):
        """Return the form class defined in the view name for the form name."""
        return self.form_classes.get(form_name, self.form_class)

    def get_forms(self, form_classes=None):
        """Return instances of the forms for form_classes to be used in this view.."""
        if form_classes is None:
            form_classes = self.get_form_classes()
        return dict(
            [key, self._create_form(key, class_name)]
            for key, class_name in form_classes.items()
        )

    def get_form(self, form_name, forms=None):
        """
        Return an instance of the form to be used in this view,
        based on the form_name value.
        """
        if forms is None:
            forms = self.get_forms()
        return forms.get(form_name)

    def get_initial(self, form_name):
        """Return the initial data to use for forms on this view."""
        return self.initials.get(form_name)

    def get_prefix(self, form_name):
        """Return the prefix to use for forms."""
        return self.prefixes.get(form_name)

    def get_prefix_from_request(self, request):
        """Return  submited form/forms prefix/s from the post request."""
        form_fields = dict.fromkeys(request.POST.keys())
        form_fields.pop('csrfmiddlewaretoken', None)
        perfixes = []
        for field in form_fields.keys():
            perfixes.append(re.match('^[^-]+', field).group(0))
        return list(dict.fromkeys(perfixes))

    def get_form_kwargs(self, form_name):
        """
        Return the keyword arguments (include prefixes defined in the view)
        for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(form_name),
            'prefix': self.get_prefix(form_name),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self, form_name):
        """
        Return the URL  of the reveresed url name. to redirect to after
        processing a valid form.
        """
        if any(self.success_urls) is False:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide at least one success_url.")
        else:
            return str(self.success_urls.get(form_name))

    def form_valid(self, form, form_name):
        """If the form is valid, redirect to the supplied URL."""
        form_valid_method = f'{form_name}_form_valid'
        if hasattr(self, form_valid_method):
            return getattr(self, form_valid_method)(form)
        success_url = self.get_success_url(form_name=form_name)
        return redirect(success_url)

    def forms_valid(self, valid_forms):
        """If multiple forms is valid, redirect to the supplied URL."""
        for form_name, form in valid_forms.items():
            success_url = self.get_success_url(form_name=form_name)
            return redirect(success_url)

    def form_invalid(self, form, form_name):
        """If the form is invalid, render the invalid form."""
        forms = {form_name: form}
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_context_data(self, form_name=None, **kwargs):
        """Insert the forms into the context dict."""
        if 'forms' not in kwargs:
            if form_name is None:
                kwargs['forms'] = self.get_forms()
            else:
                kwargs['forms'] = {form_name: self.get_form(form_name)}
        return super().get_context_data(**kwargs)

    def _create_form(self, form_name, form_class):
        """Create form instance with the assigned keyword arguments."""
        form_kwargs = self.get_form_kwargs(form_name)
        form = form_class(**form_kwargs)
        return form


class ProccessMultiFormsView(ProcessFormView):
    """Extend the ProcessFormView to proccess multiple forms."""

    def get(self, request, *args, **kwargs):
        """
        Process GET request for multiple forms.

        Returning all the forms for display in the view.
        If multiple forms are in defined in the template,
        but you want to display single form you should OVERRIDE this method.
        """
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Process POST request for multiple forms.

        Returning response for the proccesed form.
        If multiple forms are proccesed, a response from either forms is
        returned (SHOUD BE OVERRIDEN).
        """
        form_prefixes = self.get_prefix_from_request(request)
        for form_name in form_prefixes:
            return self._proccess_individual_form(form_name)

    def _proccess_individual_form(self, form_name):
        """
        Proccess the form validation and return the form_valid or invlaid
        method.
        """
        form = self.get_form(form_name)
        if not form:
            return HttpResponseForbidden("Bad Request")
        if form.is_valid():
            return self.form_valid(form, form_name)
        else:
            return self.form_invalid(form, form_name)

    def _proccess_multiple_forms(self, forms_names):
        """
        Proccess the mutliple form validation simultaneously
        and return the forms_valid or invlaid
        method.
        """
        valid_forms = {}
        invalid_forms = {}
        for form_name in forms_names:
            form = self.get_form(form_name)
            if not form:
                return HttpResponseForbidden("Bad Request")
            if form.is_valid():
                valid_forms[form_name] = form
            else:
                invalid_forms[form_name] = form
        if invalid_forms:
            for form_name, form in invalid_forms.items():
                return self.form_invalid(form, form_name)
        else:
            return self.forms_valid(valid_forms)


class BaseMultiFormsView(MultiFormsMixin, ProccessMultiFormsView):
    """A base view for displaying several forms."""


class MultiFormsView(TemplateResponseMixin, BaseMultiFormsView):
    """A view for displaying several forms, and rendering a template response."""
