# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from cinder import wsgi

# Imports for Tracelytics/Oboe
try:
    from oboeware import OboeMiddleware
    import oboe
    oboe.config['tracing_mode'] = 'always'
    oboe.config['sample_rate'] = 1.0
except ImportError:
    sys.exc_clear()
# End imports for Tracelytics/Oboe

class CinderOboeMiddleware(wsgi.Middleware):
    """Tracelytics instrumentation."""

    def __init__(self, application, *args, **kwargs):
        self._mid = OboeMiddleware(application, {}, layer='cinder')
        return super(CinderOboeMiddleware, self).__init__(application, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._mid(*args, **kwargs)
