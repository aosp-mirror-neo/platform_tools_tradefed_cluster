# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for device_history_cleaner."""

import datetime

import mock
import webtest


from tradefed_cluster import common
from tradefed_cluster import datastore_entities
from tradefed_cluster import device_info_cleaner
from tradefed_cluster import device_manager
from tradefed_cluster import testbed_dependent_test
import unittest

TIMESTAMP_1 = datetime.datetime(2024, 5, 7)
TIMESTAMP_2 = datetime.datetime(2024, 5, 8)
TIMESTAMP_3 = datetime.datetime(2024, 11, 16)  # Recent, shouldn't be hidden

_SEED_SIZE = device_info_cleaner.BATCH_SIZE * 2


class DeviceInfoCleanerTest(testbed_dependent_test.TestbedDependentTest):

  def seedDatabase(self):
    for i in range(_SEED_SIZE):
      match i % 3:
        case 0:  # Should be hidden, is gone and stale
          datastore_entities.DeviceInfo(
              device_serial=f'serial{i}',
              timestamp=TIMESTAMP_1,
              hostname=f'hostname{i}',
              state='Gone',
          ).put()
        case 1:  # Shouldn't be hidden, device is active
          datastore_entities.DeviceInfo(
              device_serial=f'serial{i}',
              timestamp=TIMESTAMP_2,
              hostname=f'hostname{i}',
              state='Available',
          ).put()
        case 2:  # Shouldn't be hidden, device was recently updated
          datastore_entities.DeviceInfo(
              device_serial=f'serial{i}',
              timestamp=TIMESTAMP_3,
              hostname=f'hostname{i}',
              state='Gone',
          ).put()

  def setUp(self):
    super().setUp()
    self.seedDatabase()

  @mock.patch.object(common, 'Now')
  @mock.patch.object(device_manager, 'HideDevice')
  def testGet(self, mock_hide_device, mock_now):
    now = datetime.datetime(2024, 11, 17)
    mock_now.return_value = now
    webapp = webtest.TestApp(device_info_cleaner.APP)

    webapp.get('/')

    # Every one in 3 entities should be hidden
    mock_hide_device.assert_has_calls(
        [
            mock.call(f'serial{i}', f'hostname{i}')
            for i in range(_SEED_SIZE) if i % 3 == 0
        ], any_order=True
    )


if __name__ == '__main__':
  unittest.main()
