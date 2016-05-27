import csv

from django.http import HttpResponse

def _get_value(obj, field):
    val = getattr(obj, field)
    if hasattr(val, '__call__'):
        val = val()
    return unicode(val).encode('utf-8', 'replace')

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None,
                         exclude=None,
                         methods=None,
                         header=True):
    """
    This function returns an export csv action
    
    @param {list} [fields=None] - works like in django ModelForm
    @param {list} [exclude=None] - works like in django ModelForm
    @param {bool} [header=True] - is whether or not to output the column names as the first row
    @param {list} [methods=None] - method names to invoke
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        if methods:
            field_names = field_names.union(set(methods))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=%s.csv" % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([_get_value(obj, field)  for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
