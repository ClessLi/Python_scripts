#/usr/bin/python3.6
from pyquery import PyQuery as pq
import os, json

sonar_pro = './sonar.pro'
if not os.path.exists(sonar_pro):
    print('%s is not exists.' % sonar_pro)
    exit(1)
def read_file(path):
    with open(path, 'r') as fp:
        return fp.readlines()

sonar_pro_list = read_file(sonar_pro)
componentKey = sonar_pro_list[0].strip('\n').split('=')[-1]
if not componentKey:
    print('Can\'t get componentKey')
    exit(1)
url = 'http://10.1.56.191:9000/api/measures/component?componentKey=%s&metricKeys=major_violations,blocker_violations,critical_violations' % componentKey
html = pq(url)
sonar_result_json = json.loads(html('p').text())
measures = sonar_result_json['component']['measures']
violations = {}
for metric in measures:
    violations.update({metric['metric'] : metric['value']})
if violations['blocker_violations'] or violations['major_violations'] or violations['critical_violations']:
    print('sonar check report: \nblocker_violations: %s, critical_violations: %s, major_violations: %s' %
          (violations['blocker_violations'],
          violations['critical_violations'],
          violations['major_violations']))
    exit(2)
else
    print('sonar check report: \nOK.')
    exit(0)