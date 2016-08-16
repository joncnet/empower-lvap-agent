#!/usr/bin/env python3
#
# Copyright (c) 2016 Roberto Riggio, Supreeth Herle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""User Equipment class."""


class UE(object):
    """User Equipment."""

    def __init__(self, rnti, vbs, config, capabilities):

        self.rnti = rnti
        self.vbsp = vbs
        self.config = config
        self.capabilities = capabilities
        self.rrc_measurements_config = config
        self.rrc_measurements = {}
        self.pcell_rsrp = None
        self.pcell_rsrq = None

    def to_dict(self):
        """ Return a JSON-serializable dictionary representing the LVAP """

        return {'rnti': self.rnti,
                'vbsp': self.vbsp.addr,
                'capabilities': self.capabilities,
                'rrc_measurements_config': self.rrc_measurements_config,
                'primary_cell_rsrp': self.pcell_rsrp,
                'primary_cell_rsrq': self.pcell_rsrq}

    def __eq__(self, other):
        if isinstance(other, UE):
            return self.rnti == other.rnti
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
