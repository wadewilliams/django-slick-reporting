from collections import OrderedDict

from django import forms
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from . import app_settings
from .helpers import get_foreign_keys


class BaseReportForm(object):
    '''
    Holds basic function
    '''

    def get_filters(self):
        """
        Get the foreign key filters for report queryset, excluding crosstab ids, handled by `get_crosstab_ids()`
        :return: a dicttionary of filters to be used with QuerySet.filter(**returned_value)
        """
        _values = {}
        if self.is_valid():
            for key, field in self.foreign_keys.items():
                if key in self.cleaned_data and not key == self.crosstab_key_name:
                    val = self.cleaned_data[key]
                    if val:
                        val = [x for x in val.values_list('pk', flat=True)]
                        _values['%s__in' % key] = val
            return None, _values

    @cached_property
    def crosstab_key_name(self):
        """
        return the actual foreignkey field name by simply adding an '_id' at the end.
        This is hook is to customize this naieve approach.
        :return: key: a string that should be in self.cleaned_data
        """
        return f'{self.crosstab_model}_id'

    def get_crosstab_ids(self):
        """
        Get the crosstab ids so they can be sent to the report generator.
        :return: 
        """
        if self.crosstab_model:
            qs = self.cleaned_data.get(self.crosstab_key_name)
            return [x for x in qs.values_list('pk', flat=True)]
        return []

    def get_crosstab_compute_reminder(self):
        return self.cleaned_data.get('crosstab_compute_reminder', True)

    def get_crispy_helper(self, foreign_keys_map=None, crosstab_model=None, **kwargs):
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Column, Layout, Div, Row, Field

        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-sm-2 col-md-2 col-lg-2'
        helper.field_class = 'col-sm-10 col-md-10 col-lg-10'
        helper.form_tag = False
        helper.disable_csrf = True
        helper.render_unmentioned_fields = True

        foreign_keys_map = foreign_keys_map or self.foreign_keys

        helper.layout = Layout(
            Row(
                Column(
                    Field('start_date'), css_class='col-sm-6'),
                Column(
                    Field('end_date'), css_class='col-sm-6'),
                css_class='raReportDateRange'),
            Div(css_class="mt-20", style='margin-top:20px')
        )

        # first add the crosstab model and its display reimder then the rest of the fields
        if self.crosstab_model:
            helper.layout.fields[1].append(Field(self.crosstab_key_name))
            if self.crosstab_display_compute_reminder:
                helper.layout.fields[1].append(Field('crosstab_compute_reminder'))

        for k in foreign_keys_map:
            if k != self.crosstab_key_name:
                helper.layout.fields[1].append(Field(k))

        return helper


def _default_foreign_key_widget(f_field):
    return {'form_class': forms.ModelMultipleChoiceField,
            'required': False, }


def report_form_factory(model, fkeys_filter_func=None, foreign_key_widget_func=None, crosstab_model=None,
                        display_compute_reminder=True, **kwargs):
    """
    Create a Reprot Form based on the report_model passed
    
    :param model: 
    :param fkeys_filter_func: 
    :param foreign_key_widget_func: 
    :param crosstab_model: 
    :param display_compute_reminder: 
    :param kwargs: 
    :return: 
    """
    foreign_key_widget_func = foreign_key_widget_func or _default_foreign_key_widget
    fkeys_filter_func = fkeys_filter_func or (lambda x: x)

    # gather foreign keys
    fkeys_map = get_foreign_keys(model)
    fkeys_map = fkeys_filter_func(fkeys_map)

    fkeys_list = []
    fields = OrderedDict()

    fields['start_date'] = forms.DateTimeField(required=False, label=_('From date'),
                                               initial=app_settings.SLICK_REPORTING_DEFAULT_START_DATE,
                                               widget=forms.DateTimeInput(
                                                   attrs={'autocomplete': "off"}),
                                               )

    fields['end_date'] = forms.DateTimeField(required=False, label=_('To  date'),
                                             initial=app_settings.SLICK_REPORTING_DEFAULT_END_DATE,
                                             widget=forms.DateTimeInput(
                                                 attrs={'autocomplete': "off"})
                                             )

    for name, f_field in fkeys_map.items():
        fkeys_list.append(name)

        fields[name] = f_field.formfield(
            **foreign_key_widget_func(f_field))

    if crosstab_model and display_compute_reminder:
        fields['crosstab_compute_reminder'] = forms.BooleanField(required=False,
                                                                 label=_('display the crosstab reminder'),
                                                                 initial=True)

    new_form = type('ReportForm', (BaseReportForm, forms.BaseForm,),
                    {"base_fields": fields,
                     '_fkeys': fkeys_list,
                     'foreign_keys': fkeys_map,
                     'crosstab_model': crosstab_model,
                     'crosstab_display_compute_reminder': display_compute_reminder,
                     })
    return new_form
