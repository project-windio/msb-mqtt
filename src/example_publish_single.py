#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This shows an example of using the publish.single helper function.

# Example has been changed to publish at the same host where we also subscribe using
# the example_subscript.py script.

import paho.mqtt.publish as publish

publish.single("encyclopedia/windio", "boo", hostname="broker.mqttdashboard.com")
