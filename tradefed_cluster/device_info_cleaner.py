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

"""Module for device info "cleaning" cron job."""

import datetime
import logging

import flask


from tradefed_cluster import common
from tradefed_cluster import device_manager
from tradefed_cluster import datastore_entities
from tradefed_cluster.util import ndb_shim as ndb

# Hide devices that have been gone for 15 days without any events.
AUTO_HIDE_GONE_DAYS = 15
BATCH_SIZE = 200
DEFAULT_DEADLINE = 60  # Query deadline in seconds

# The GAE frontend timeout is 10 minutes. So let's restart the request after
# 8 minutes.
TIMEOUT_MINUTES = 8

APP = flask.Flask(__name__)


def RetrieveEntities(end_date):
  """Retrieve Entities keys that are older than a given end date.

  The keys are yielded in batches to reduce the likelyhood of timeouts.

  Args:
    end_date: date to compare against the DeviceInfo timestamp

  Yields:
    Lists of keys older than the given end_date.
  """
  while True:
    query = datastore_entities.DeviceInfo.query(
        datastore_entities.DeviceInfo.timestamp < end_date
    )
    query = query.filter(datastore_entities.DeviceInfo.hidden == False)  
    query = query.filter(
        datastore_entities.DeviceInfo.state == common.DeviceState.GONE)

    entities = []
    # Do not use the cache as the keys are being retrieved for deletion.
    for entity in query.iter(
        limit=BATCH_SIZE,
        projection=[
            datastore_entities.DeviceInfo.device_serial,
            datastore_entities.DeviceInfo.hostname],
        use_cache=False,
        use_memcache=False,
        deadline=DEFAULT_DEADLINE,
    ):
      entities.append(entity)
    yield entities
    if len(entities) < BATCH_SIZE:
      break


def HideDeviceInfos(retention_days):
  """Hide DeviceInfo entities older than the retention days.

  Args:
    retention_days: Number of days to keep in datastore.

  Returns:
    Number of entities hidden.
  """
  now = common.Now()
  end_date = now - datetime.timedelta(days=retention_days)
  request_end_time = now + datetime.timedelta(minutes=TIMEOUT_MINUTES)
  hidden = 0
  for device_info_entities in RetrieveEntities(end_date):
    for device_info in device_info_entities:
      try:
        device_manager.HideDevice(
            device_info.device_serial, device_info.hostname
        )
        hidden += 1
        if common.Now() > request_end_time:
          logging.info("End the request after %r minutes.", TIMEOUT_MINUTES)
          return hidden
      except ndb.exceptions.Error:
        logging.exception("Datastore error while hiding a device.")
  return hidden


@APP.route("/")
@APP.route("/<path:fake>")
def HideGoneDevices(fake=None):
  """Hiding device info."""
  del fake
  logging.info("Started HideGoneDevices")
  number_deleted = HideDeviceInfos(AUTO_HIDE_GONE_DAYS)
  logging.info("Finished HideGoneDevices. Deleted: %d", number_deleted)
  return str(number_deleted)
