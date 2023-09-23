# python lib
import csv
import os
import re

import tempfile
import xlrd
from docxtpl import DocxTemplate
import xlwt
import os.path;
# django lib

from django.http import HttpResponse
from django.db import IntegrityError
from django.conf import settings
from rest_framework import generics, mixins
from .exception_handler import DataError, InvalidFile
from django.db.models import Field, ForeignKey, ForeignObjectRel, ManyToManyField


def nested_getattr(obj, attribute, split_rule='__'):
    """
    This function is responsible for getting the nested record from the given obj parameter
    :param obj: whole item without splitting
    :param attribute: field after splitting
    :param split_rule:
    :return:
    """
    split_attr = attribute.split(split_rule)
    for attr in split_attr:
        if not obj:
            break
        obj = getattr(obj, attr)

    return obj


def export_to_csv(queryset, fields, titles, file_name):
    """
    will export the model data in the form of csv file
    :param queryset: queryset that need to be exported as csv
    :param fields: fields of a model that will be included in csv
    :param titles: title for each cell of the csv record
    :return:
    """
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force downloadmodel
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
    # the csv writer
    writer = csv.writer(response)
    if fields:
        headers = fields
        if titles:
            titles = titles
        else:
            titles = headers
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        titles = headers

    # Writes the title for the file
    writer.writerow(titles)

    # write data rows
    for item in queryset:
        writer.writerow([nested_getattr(item, field) for field in headers])
    return response


def export_to_pdf(text):
    pass


def render_template_docs(template_file_path, context: dict):
    """
       This method complete template docx with context informations.

       Parameters
       -------
       template_file : File
            This param contains template docx to complete,
       context: Dict
            This parm contains the informations to complete,
       Returns
       -------
       File
           file competed with informations.
    """
    assert template_file_path, 'template_file_path is required'
    # check if file exist
    if not os.path.isfile(template_file_path):
        raise Exception('Template File Not Found ')

    context = context or {}

    doc = DocxTemplate(template_file_path)

    doc.render(context)
    return doc


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class GenerateDocumentView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    GenerateAutorizationForm allow to generate an autorization form document filled with values.
    """
    template_path = os.path.join(settings.PROJECT_ROOT, 'static/test_generation.docx')

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {'object': instance}
        doc = render_template_docs(self.template_path, context)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file_name = self.get_object().__str__()
        response['Content-Disposition'] = 'attachment; filename={}.docx'.format(file_name)
        doc.save(response)
        return response


def export_xlsx(queryset, fields, titles, file_name, sheet_name):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(sheet_name)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(titles)):
        ws.write(row_num, col_num, titles[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = queryset
    for row in rows:
        row_num += 1

        for col_num in range(len(fields)):
            # print("****************************************")
            # print(fields[col_num])
            # print(str(nested_getattr(row, fields[col_num])))
            ws.write(row_num, col_num, str(nested_getattr(row, fields[col_num])), font_style)
    wb.save(response)
    return response


def import_xlsx(excel_file, fields, model):
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(excel_file.read())
    try:
        book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
    except xlrd.XLRDError:
        raise InvalidFile
    object_kwargs = dict()
    row_num = 0
    col_index = 0
    m_list = []
    try:
        for rx in range(1, sh.nrows):
            row_num += 1
            for col_num in range(len(fields)):
                field = fields[col_num].get('field_name')
                print("**************** field ****************")
                print(fields[col_num].get('field_name'))
                field_object = model._meta.get_field(fields[col_num].get('field_name'))
                if isinstance(field_object, Field) \
                        and not isinstance(field_object, ForeignKey) \
                        and not isinstance(field_object, ManyToManyField):
                    print("********************* Simple Field ********** ")
                    object_kwargs[field] = sh.cell(rx, col_num).value
                if isinstance(field_object, ForeignKey):
                    print("********************* Foreign key Field ********** ")
                    object_model = field_object.related_model
                    object = get_object(object_model,
                                        fields[col_num].get('search_criterion'),
                                        sh.cell(rx, col_num).value)
                    object_kwargs[field] = object

                if isinstance(field_object, ManyToManyField) or isinstance(field_object, ForeignObjectRel):
                    print("********************* Many To Many Field ********** ")
                    related_model = field_object.related_model
                    item = fields[col_num]
                    item['index'] = col_num
                    item['target_field'] = fields[col_num].get('field_name')
                    item['related_model'] = related_model
                    m_list.append(item)

            object_instance = model(**object_kwargs)
            object_instance.save()

            for m2m_related_object in m_list:
                array_object_str = sh.cell(rx, m2m_related_object.get('index')).value.strip().replace(" ","")
                splitted_array = array_object_str[1:][:-1].split(',')
                if len(splitted_array) > 1:
                    for obj_str in splitted_array:
                        add_object_to_set(m2m_related_object.get('related_model'),
                                                model,
                                                object_instance,
                                                m2m_related_object.get('target_field'),
                                                m2m_related_object.get('search_criterion'),
                                                obj_str
                                                )
    except IntegrityError:
        raise DataError


def add_object_to_set(related_model, model, instance, target_field, search_criterion, search_value):
    search_value = search_value.replace("'", "")
    kwargs_filter = dict()
    kwargs_filter[search_criterion] = search_value
    related_object = related_model.objects.filter(**kwargs_filter).first()
    if related_object:
        output = getattr(instance, target_field)
        output.add(related_object)
    else:
        raise DataError


def get_object(model, search_criterion, search_value):
    kwargs_filter = dict()
    kwargs_filter[search_criterion] = search_value
    related_object = model.objects.filter(**kwargs_filter).first()
    return related_object










