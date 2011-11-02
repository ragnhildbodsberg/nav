#
# Copyright (C) 2011 UNINETT AS
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 2 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.  You should have received a copy of the GNU General Public License
# along with NAV. If not, see <http://www.gnu.org/licenses/>.
#
"""SeedDB Django URL config"""

from django.conf.urls.defaults import patterns, url

from nav.web.maintenance.views import active, planned, historic

dummy = lambda *args, **kwargs: None

urlpatterns = patterns('',
    url(r'^$', dummy,
        name='maintenance'),
    url(r'^calendar/$', dummy,
        name='maintenance-calendar'),
    url(r'^active/$', active,
        name='maintenance-active'),
    url(r'^planned/$', planned,
        name='maintenance-planned'),
    url(r'^historic/$', historic,
        name='maintenance-historic'),
    url(r'^new/$', dummy,
        name='maintenance-new'),
    url(r'^view/(?P<task_id>\d+)/$', dummy,
        name='maintenance-view'),

    url(r'^new\?netbox=(?P<netbox_id>\d+)$', dummy,
        name='maintenance-new-netbox'),
    url(r'^new\?service=(?P<service_id>\d+)$', dummy,
        name='maintenance-new-service'),
)
