import urllib.request
import urllib.parse
from pyquery import PyQuery as pq

def url_open(url, data=None):
    req = urllib.request.Request(url, data)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
    req_data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return req_data

def get_site_abb():
    """
    获取12306各站点名及缩写
    :return: site_names_dict
    """
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8392'
    result = url_open(url)
    result_pq = pq(result)
    #print(result_pq('p').text())
    data = result_pq('p').text().split("'")
    site_names_set = set(data[1].split('@'))
    site_names_dict = {}
    for i in site_names_set:
        #print(i)
        if i == '':
            continue
        site_name = str(i).split('|')
        site_names_dict.update({site_name[1]: site_name[2]})
    #print(site_names_dict)
    return site_names_dict


if __name__ == '__main__':
    site_names_dict = get_site_abb()
    print(site_names_dict)