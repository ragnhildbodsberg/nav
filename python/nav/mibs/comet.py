#
# Copyright (C) 2014 UNINETT
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.  You should have received a copy of the GNU General Public License
# along with NAV. If not, see <http://www.gnu.org/licenses/>.
#
"""A class for getting temperature sensors/channels from a Comet P8541.

Comet's MIBs are highly disorganized and illogical, so any other model will
need a separate implementation, or a workaround to make a more generic
implementation for multiple MIBs must be implemented.

"""

from twisted.internet import defer
from twisted.internet.defer import returnValue
from nav.mibs.mibretriever import MibRetriever

DEGREES_CELSIUS = "\xb0C"
DEGREES_FAHRENHEIT = "\xb0F"
UNIT_MAP = {
    DEGREES_CELSIUS: "Celsius",
    DEGREES_FAHRENHEIT: "Fahrenheit",
}


class Comet(MibRetriever):
    """MibRetriever for Comet Web Sensors"""
    from nav.smidumps.p8652_mib import MIB as mib

    def get_module_name(self):
        """Returns the MIB module name"""
        return self.mib.get('moduleName', None)

    @defer.inlineCallbacks
    def get_all_sensors(self):
        """Discovers and returns all eligible sensors from the Comet MIB on this
        device.
        """
        channels = yield self.get_channels()
        bin_inputs = yield self.get_binary_inputs()
        returnValue(channels + bin_inputs)

    @defer.inlineCallbacks
    def get_channels(self):
        """Returns the temperature sensor channels for this probe."""
        self._logger.info("collecting Comet channels")
        result = []
        for channel in range(1, 5):
            o_name = "ch%dName" % channel
            o_unit = "ch%dUnit" % channel
            o_value = "ch%dIntVal" % channel
            value_oid = self.nodes[o_value].oid

            name = yield self.get_next(o_name)
            unit = yield self.get_next(o_unit)
            unit = UNIT_MAP.get(unit, unit)
            self._logger.debug("channel %s name/unit: %r/%r",
                               channel, name, unit)

            result.append(dict(
                oid=str(value_oid) + '.0',
                unit_of_measurement=unit,
                precision=1,
                scale=None,
                description=name,
                name="Channel %s" % channel,
                internal_name="channel%s" % channel,
                mib=self.get_module_name(),
            ))
        returnValue(result)

    @defer.inlineCallbacks
    def get_binary_inputs(self):
        """Returns the binary inputs of this probe, also their alarm status"""
        self._logger.info("collecting Comet binary sensors")
        result = []
        for binary in range(1, 4):
            o_name = "bin%dName" % binary
            o_value = "bin%dIntVal" % binary
            o_alarm = "bin%dAlarm" % binary
            value_oid = self.nodes[o_value].oid
            alarm_oid = self.nodes[o_alarm].oid

            name = yield self.get_next(o_name)
            value = yield self.get_next(o_value)
            if value is None:
                self._logger.info("Ignoring BIN input %s (%s), it has no value",
                                  binary, name)
                continue
            self._logger.debug("BIN input %s name: %r", binary, name)

            result.append(dict(
                oid=str(value_oid) + '.0',
                unit_of_measurement="boolean",
                precision=0,
                scale=None,
                description=name,
                name="BIN %s" % binary,
                internal_name="bin%s" % binary,
                mib=self.get_module_name(),
            ))
            result.append(dict(
                oid=str(alarm_oid) + '.0',
                unit_of_measurement="boolean",
                precision=0,
                scale=None,
                description="%s alarm" % name,
                name="BIN %s Alarm" % binary,
                internal_name="bin%sAlarm" % binary,
                mib=self.get_module_name(),
            ))
        returnValue(result)
