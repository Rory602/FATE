#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from .transfer import FederationBuilder
__all__ = ["FederationBuilder", "Cleaner"]


class Cleaner(object):
    def __init__(self):
        self._tables = []
        self._kv = {}

    def add_table(self, table):
        self._tables.append(table)

    def add_obj(self, table, key):
        if (table._name, table._namespace) not in table:
            self._kv[(table._name, table._namespace)] = (table, [])
        else:
            self._kv[(table._name, table._namespace)][1].append(key)

    def clean(self):
        for table in self._tables:
            try:
                table.destroy()
            except:
                pass

        for _, (table, keys) in self._kv.items():
            for key in keys:
                try:
                    table.delete(key)
                except:
                    pass

