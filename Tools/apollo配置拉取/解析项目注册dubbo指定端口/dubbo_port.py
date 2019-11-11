#!/usr/bin/python3.6
import configparser
import json
import sys
from pyquery import PyQuery as pq


def usage():
    print("Plz Usage: %s <Project Name> <ENV> (e.g. %s Template_tomcat_nodejs_uatd uat)" % (sys.argv[0], sys.argv[0]))


def checkArgs():
    if len(sys.argv) < 3:
        usage()
        exit(1)
    if sys.argv[2].lower() not in ("dev", "uat", "sit", "sandbox", "perform"):
        usage()
        exit(1)


def confUrl(env, appid, cname, ns):
    if env == 'dev':
        apollo_socket = "10.1.56.172:9090"
    elif env == 'sit':
        apollo_socket = "10.1.52.172:9090"
    elif env == 'uat':
        apollo_socket = "10.1.48.172:9090"
    elif env == 'sandbox':
        apollo_socket = "10.1.60.172:9090"
    elif env == 'perform':
        apollo_socket = "10.1.76.97:9090"
    else:
        return False
    url = "http://%s/configs/%s/%s/%s" % (apollo_socket, appid, cname, ns)
    return url


def getDubboPort(projectName, confPath, env):
    conf = configparser.ConfigParser()
    conf.read(confPath)
    appID = conf[projectName]["APOLLO_APP_ID"]
    # nameSpace = conf[projectName]["APOLLO_NAMESPACE"]
    nameSpace = "application"
    # clusterName = conf[projectName]["APOLLO_CLUSTER"]
    clusterName = "default"
    config_url = confUrl(env, appID, clusterName, nameSpace)
    if config_url:
        appConfJson = json.loads(pq(config_url)('p').text())
        port = appConfJson.get("configurations").get("dubbo.provider.port")
        if port:
            return port
        else:
            return None
    else:
        return False


if __name__ == "__main__":
    checkArgs()
    confPath = "/home/shell/docker/docker.ini"
    projectName = sys.argv[1]
    env = sys.argv[2].lower()
    dubboPort = getDubboPort(projectName, confPath, env)
    if dubboPort:
        print(dubboPort)