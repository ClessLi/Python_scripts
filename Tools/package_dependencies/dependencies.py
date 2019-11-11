# encoding:utf-8

import json

def parse_package(dict_json, package, version):
    if isinstance(dict_json, dict):
        for key in dict_json:
            if key == package:
                if isinstance(dict_json[key], dict):
                    version2 = dict_json[key].get('version')
                elif isinstance(dict_json[key], str):
                    version2 = dict_json[key]
                else:
                    print(dict_json[key])
                    return False
                return check_version(key, version, version2)
            else:
                if isinstance(dict_json[key], dict):
                    parse_package(dict_json[key], package, version)
                else:
                    continue

def parse_package_new(dic_jaon, package, version):

def check_version(key, ver1, ver2):
    if str(ver1).strip('^') == str(ver2).strip('^'):
        return None
    else:
        #print('package:%s version1:%s version2:%s' % (key, ver1, ver2))
        print(key)
        return key


if __name__ == "__main__":
    package_dict = {}
    package_de_dict

    try:
        with open('.\package.json') as json1:
            json_data1 = json.load(json1)
            package_dict.update(json_data1.get('dependencies'))
            package_dict.update(json_data1.get('devDependencies'))
            print(package_dict)
            #update_packages = []
            with open('.\package-lock.json') as json2:
                json_data2 = json.load(json2)
                for key in package_dict:
                    #print('%s：%s' % (key, parse_package(json_data2, key, package_dict[key])))
                    package = parse_package(json_data2, key, package_dict[key])
                    #print(package)
                    #if package:
                        #update_packages.append(package)
                #print(update_packages)
    except Exception as err:
        print(err)
        exit()

