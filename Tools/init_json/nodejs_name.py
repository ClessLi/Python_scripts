import json
import sys


def init_json(string):
    json_str = string.strip('\n').strip(';').replace('\'', '\"')
    print(json_str)
    json_dict = json.loads(json_str[json_str.index('{'):])
    return json_dict


if __name__ == '__main__':
    try:
        #s1 = sys.argv[1]
        s1 = '''module.exports = {
  "apps": [{
    "name": "react-fmious",
    "script": "./index.js",
    "watch": ["app/server", "node_modules/@mitan-static", "node_modules/@mitan-template"],
    "node_args": "--harmony",
    "merge_logs": true,
    "cwd": "./",
    "instances": 1,
    "exec_mode": "cluster",
    "env": {
      "CONFIG": 'config/config.uatl.js'
    }
  }]
};'''
    except Exception as err:
        print('[ERROR] %s\nPlease usage: %s <data(str)>' % (err, sys.argv[0]))
        exit()

    names = []
    json_dict = init_json(s1)
    for item in json_dict['apps']:
        names.append(item['name'])
    print(' '.join(names))
    #sys.stdout(' '.join(names))
