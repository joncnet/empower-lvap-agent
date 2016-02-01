#!/usr/bin/env python3
#
# Copyright (c) 2015, Roberto Riggio
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the CREATE-NET nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CREATE-NET ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CREATE-NET BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""RYU Connector."""

import json
import http.client

from empower.core.jsonserializer import EmpowerEncoder
from urllib.parse import urlparse

import empower.logger
LOG = empower.logger.get_logger()


class RyuFlowEntry():

    def __init__(self, server="localhost", port=8080):

        self.server = server
        self.port = port

    def add_station_flows(self, lvap_addr, dpid, port_id):

        match = {
            "hwaddr": lvap_addr,
            "src_dpid": dpid,
            "src_port": port_id
        }

        LOG.info("LVAP %s is at %s / %u" % (lvap_addr, dpid, port_id))

        body = json.dumps(match, indent=4, cls=EmpowerEncoder)

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }

        try:

            conn = http.client.HTTPConnection(self.server, self.port)
            conn.request("POST", "/simpleswitch/vnfrule/", body, headers)
            response = conn.getresponse()

            ret = (response.status, response.reason, response.read())
            LOG.info("Result: %u %s" % (ret[0], ret[1]))
            conn.close()

            return response.getheader("Location", None)

        except:

            LOG.error("Connection refused.")

    def remove_station_flows(self, location):

        LOG.info("LVAP removing flows %s" % location)

        try:

            tokens = urlparse(location).path.split("/")

            conn = http.client.HTTPConnection(self.server, self.port)
            conn.request("DELETE", "/simpleswitch/vnfrule/%s" % tokens[-1])
            response = conn.getresponse()

            ret = (response.status, response.reason, response.read())
            LOG.info("Result: %u %s" % (ret[0], ret[1]))
            conn.close()

        except:

            LOG.error("Connection refused.")
