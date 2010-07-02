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

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import update_object

from nav.models.cabling import Cabling, Patch
from nav.models.manage import Netbox, NetboxType, Room, Location, Organization, Usage, Vendor, Subcategory, Vlan, Prefix
from nav.models.service import Service
from nav.web.message import new_message, Messages

from nav.web.seeddb.forms import *
from nav.web.seeddb.utils import render_seeddb_list, form_magic

NAVPATH_DEFAULT = [('Home', '/'), ('Seed DB', '/seeddb/')]

def index(request):
    return render_to_response(
        'seeddb/index.html',
        {
            'title': 'Seed Database',
            'navpath': [('Home', '/'), ('Seed DB', None)],
        },
        RequestContext(request)
    )

def netbox_list(request):
    qs = Netbox.objects.all()
    value_list = (
        'sysname', 'room', 'ip', 'category', 'organization', 'read_only',
        'read_write', 'type__name', 'device__serial'
    )
    extra = {
        'title': 'Seed IP devices',
        'navpath': NAVPATH_DEFAULT + [('IP Devices', None)],
    }

    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-netbox-edit', edit_url_attr='sysname',
        extra_context=extra)

def service_list(request):
    qs = Service.objects.all()
    value_list = ('netbox__sysname', 'handler', 'version')
    extra = {
        'title': 'Seed services',
        'navpath': NAVPATH_DEFAULT + [('Services', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-service-edit', extra_context=extra)

def room_list(request):
    qs = Room.objects.all()
    value_list = (
        'id', 'location', 'description', 'optional_1', 'optional_2',
        'optional_3', 'optional_4')
    extra = {
        'title': 'Seed rooms',
        'navpath': NAVPATH_DEFAULT + [('Rooms', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-room-edit', extra_context=extra)

def room_edit(request, room_id=None):
    room = None
    if room_id:
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return HttpResponseRedirect(reverse('seeddb-room-edit'))
    if request.method == 'POST':
        if room:
            pass
        else:
            pass
    return

def location_list(request):
    qs = Location.objects.all()
    value_list = ('id', 'description')
    extra = {
        'title': 'Seed Locations',
        'navpath': NAVPATH_DEFAULT + [('Locations', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-location-edit', extra_context=extra)

def location_edit(request, location_id=None):
    return form_magic(
        request, LocationForm, Location, location_id,
        error_redirect='seeddb-location-edit',
        save_redirect='seeddb-location-edit',
        extra_context={
            'navpath': NAVPATH_DEFAULT + [('Locations', reverse('seeddb-location'))],
        }
    )

def organization_list(request):
    qs = Organization.objects.all()
    value_list = (
        'id', 'parent', 'description', 'optional_1', 'optional_2',
        'optional_3')
    extra = {
        'title': 'Seed Organizations',
        'navpath': NAVPATH_DEFAULT + [('Organizations', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-organization-edit', extra_context=extra)

def usage_list(request):
    qs = Usage.objects.all()
    value_list = ('id', 'description')
    extra = {
        'title': 'Seed Usage Categories',
        'navpath': NAVPATH_DEFAULT + [('Usage categories', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-usage-edit', extra_context=extra)

def type_list(request):
    qs = NetboxType.objects.all()
    value_list = (
        'name', 'vendor', 'description', 'sysobjectid', 'frequency', 'cdp',
        'tftp')
    extra = {
        'title': 'Seed Types',
        'navpath': NAVPATH_DEFAULT + [('Types', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-type-edit', extra_context=extra)

def vendor_list(request):
    qs = Vendor.objects.all()
    value_list = ('id',)
    extra = {
        'title': 'Seed Vendors',
        'navpath': NAVPATH_DEFAULT + [('Vendors', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-vendor-edit', extra_context=extra)

def subcategory_list(request):
    qs = Subcategory.objects.all()
    value_list = ('id', 'category', 'description')
    extra = {
        'title': 'Seed Subcategories',
        'navpath': NAVPATH_DEFAULT + [('Subcategories', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-subcategory-edit', extra_context=extra)

def vlan_list(request):
    qs = Vlan.objects.all()
    value_list = ('id', 'vlan', 'net_type', 'organization', 'usage', 'net_ident', 'description')
    extra = {
        'title': 'Seed Vlan',
        'navpath': NAVPATH_DEFAULT + [('Vlan', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-vlan-edit', extra_context=extra)

def prefix_list(request):
    qs = Prefix.objects.filter(vlan__net_type__edit=True)
    value_list = (
        'net_address', 'vlan__net_type', 'vlan__organization',
        'vlan__net_ident', 'vlan__usage', 'vlan__description', 'vlan__vlan')
    extra = {
        'title': 'Seed Prefix',
        'navpath': NAVPATH_DEFAULT + [('Prefix', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-prefix-edit', extra_context=extra)

def cabling_list(request):
    qs = Cabling.objects.all()
    value_list = ('room', 'jack', 'building', 'target_room', 'category', 'description')
    extra = {
        'title': 'Seed Cabling',
        'navpath': NAVPATH_DEFAULT + [('Cabling', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-cabling-edit', extra_context=extra)

def patch_list(request):
    qs = Patch.objects.all()
    value_list = ('interface__netbox', 'interface__module', 'interface__baseport', 'cabling__room', 'cabling__jack', 'split')
    extra = {
        'title': 'Seed Patch',
        'navpath': NAVPATH_DEFAULT + [('Patch', None)],
    }
    return render_seeddb_list(request, qs, value_list,
        edit_url='seeddb-patch-edit', extra_context=extra)
