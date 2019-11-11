#!/usr/bin/python3.6
# encoding:utf-8
# Authored by Cless Li, at 2019/08/29
import sys
import os
import json
from properties import Properties, replace_property
from updateXml import Xml


class Config(object):
    def update(self):
        update_log = "Start updating the local config file of '%s'" % self._configPath
        self._output_log(update_log)
        for active in self.actives:
            self._update(active)
        complete_log = "Update completely on the local config file of '%s'" % self._configPath
        self._output_log(complete_log)
        # if self.active.get('delete'):
        #     for key in self.active['delete']:

    def _output_log(self, log, flag='=', flag_num=150):
        log_flag = (int(flag_num) - len(log)) // 2
        print("%s%s%s" % (flag*log_flag, log, flag*log_flag))

    def _update(self, active):
        if self._configType == 'properties':
            return self._properties_update(active)
        elif self._configType == 'xml':
            return self._xml_update(active)
        else:
            raise TypeError(
                "The [%s] configType Error!" % self._configType
            )

    def _properties_update(self, active):
        if self.actives.get(active):
            for key in self.actives[active]:
                if active == 'update':
                    value = self.actives[active].get(key)
                    self._config.set(key, value)
                elif active == 'delete':
                    self._config.remove(key)

    def _xml_update(self, active):
        if self.actives.get(active):
            # print(active)
            for xmlpath in self.actives[active]:
                # print(self.actives[active], type(self.actives[active]))
                if isinstance(self.actives[active], list):
                    values = None
                    self._config.update_config(active, xmlpath, values)
                else:
                    values = self.actives[active].get(xmlpath)
                    # print(values, type(values), isinstance(values, list))
                    if isinstance(values, list):
                        for value in values:
                            # print(value)
                            self._config.update_config(active, xmlpath, value)
                    else:
                        self._config.update_config(active, xmlpath, values)
        self._config.write_config()

    def _init_config(self, conf_json):
        if self._configType == 'xml':
            return Xml(self._configPath, self._configPath)
        elif self._configType == 'properties':
            return Properties(self._configPath)
        else:
            raise TypeError(
                "The [%s] configType Error!" % self._configType
            )

    def __init__(self, update_json):
        self._configPath = os.path.basename(update_json.get('configPath'))
        self._configType = update_json.get('configType')
        self._config = self._init_config(update_json)
        self.actives = update_json.get('active')


def update(json_data):
    for item in json_data:
        config = Config(item)
        config.update()


if __name__ == '__main__':
    jsonPath = 'configUpdate.json'
    # if len(sys.argv) >= 2:
    #     jsonPath = sys.argv[1]
    # else:
    #     jsonPath = ''
    #     print("Plz usage: %s <update_json_path>" % sys.argv[0])
    #     exit(1)
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r', encoding='utf-8') as json_fp:
            updateJsonData = json.load(json_fp)
            if updateJsonData:
                update(updateJsonData)