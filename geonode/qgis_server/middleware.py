# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################


class QGISServerLayerMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    # def process_exception(self, request, exception):
    #     return HttpResponse("in exception")

    def process_template_response(self, request, response):
        """Middleware to add more context for QGIS Server backend app.

        :type request: django.http.request.HttpRequest
        :type response: django.template.response.TemplateResponse
        """

        template_name = response.template_name
        if template_name == 'layers/layer_detail.html':
            self.layer_detail(request, response)

        return response

    def layer_detail(self, request, response):
        """Provide more context for layer_detail view

        :type request: django.http.request.HttpRequest
        :type response: django.template.response.TemplateResponse
        """
        context = response.context_data

        if 'resource' in context:
            # provides context for QML Style
            layer = context['resource']
            """:type: geonode.layers.models.Layer"""
            use_qml_style = layer.upload_session.layerfile_set.filter(
                name='qml').count() > 0

            context['use_qml_style'] = use_qml_style
