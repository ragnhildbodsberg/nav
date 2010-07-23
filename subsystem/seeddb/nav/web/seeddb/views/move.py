# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 UNINETT AS
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

from IPy import IP
from socket import gethostbyname, gethostbyaddr

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from nav.models.cabling import Cabling, Patch
from nav.models.manage import Netbox, NetboxType, Room, Location, Organization, Usage, Vendor, Subcategory, Vlan, Prefix
from nav.models.service import Service
from nav.web.message import new_message, Messages
from nav.Snmp import Snmp

from nav.web.seeddb.forms.move import *
from nav.web.seeddb.utils.move import *

TITLE_DEFAULT = 'NAV - Seed Database'
NAVPATH_DEFAULT = [('Home', '/'), ('Seed DB', '/seeddb/')]

def netbox_move(request):
    extra = {
        'navpath': NAVPATH_DEFAULT + [('IP Devices', reverse('seeddb-netbox'))],
        'tab_template': 'seeddb/tabs_netbox.html',
    }
    return move(request, Netbox, NetboxMoveForm, 'seeddb-netbox',
        title_attr='sysname',
        extra_context=extra)

def room_move(request):
    extra = {
        'navpath': NAVPATH_DEFAULT + [('Room', reverse('seeddb-room'))],
        'tab_template': 'seeddb/tabs_room.html',
    }
    return move(request, Room, RoomMoveForm, 'seeddb-room',
        extra_context=extra)

def organization_move(request):
    extra = {
        'navpath': NAVPATH_DEFAULT + [('Organization', reverse('seeddb-organization'))],
        'tab_template': 'seeddb/tabs_organization.html',
    }
    return move(request, Organization, OrganizationMoveForm, 'seeddb-organization',
        extra_context=extra)
