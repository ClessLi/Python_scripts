"""
@初始配置项
Author:韦玮
Upgrade by Cless Li
---------------
"""
# 12306账号
myuser = "13647633961"
mypasswd = "ab19881218"
import urllib.request
import re
import ssl
import urllib.parse
import http.cookiejar
import datetime
import time
from pyquery import PyQuery as pq
import json



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

def check_ticks(date, start, to, student):
    """
    余票查询
    :param date: 查询日期
    :param start: 出发站
    :param to: 到达站
    :param student: 是否为学生票
    :return: 无
    """
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + start + "&leftTicketDTO.to_station=" + to + "&purpose_codes=" + student
    data = pq(url)('p').text()
    data_init = json.loads(data)
    #  print(data_init)
    allcheci = data_init['data']['result']
    checimap = data_init['data']['map']
    # print(checimap)
    print("车次\t|出发站名\t|到达站名\t|出发时间\t|到达时间\t|一等座\t|二等座\t|硬座\t|无座")
    for item in allcheci:
        try:
            # print(item, type(item))
            '''
            |预订|620000K5020B|K503|CSQ|ICW|CUW|ICW|06:43|10:53|04:10|Y|NfxWWt7keirSrjQqPGEMCbam2gYP8mYXiuY0liVGbv4Uu0aqBsBqYfsg9fE%3D|(13)20180819|3|Q6|08|09|0|0||||(23软卧)5|||(26无座)6||有|有|||||10401030|1413|0
            |预订|77000G859400|G8594|CXW|ICW|CXW|ICW|06:52|08:11|01:19|Y|%2Fh3Q%2F6o1WoRyc8stHuyI4EWGpyBuSYUH64i1hoz1nchv5f6n|(13)20180820|3|W1|01|02|0|0||||(23软卧)||(25商务)有|(26无座)||||有|有|||O0M0P0|OMP|0
            |预订|77000G223200|G2232|CXW|EAY|CXW|ICW|07:01|08:18|01:17|Y|Lljq13X6IChWIKGl7596wBfBSCkMy0%2FuCPTpt2Ll7%2Bafzxpj|20180820|3|W1|01|02|0|0||||(23软卧)|||(26无座)||(28硬卧)|(29硬座)|(30二等)有|(31一等)无|(32特等)无||O0M090|OM9|0
            '''
            thischeci = item.split("|")
            # [3]---code
            code = thischeci[3]
            # [6]---fromname
            fromname = thischeci[6]
            # print(fromname)
            fromname = checimap[fromname]
            # [7]---toname
            toname = thischeci[7]
            toname = checimap[toname]
            # [8]---stime
            stime = thischeci[8]
            # [9]---atime
            atime = thischeci[9]
            # [28]---yz
            yz = thischeci[29]
            # [29]---wz
            wz = thischeci[26]
            # [30]---ze
            ze = thischeci[30]
            # [31]---zy
            zy = thischeci[31]
            print(code + "\t|" + fromname + "\t|" + toname + "\t|" + stime + "\t|" + atime + "\t|" + str(
                zy) + "\t|" + str(ze) + "\t|" + str(yz) + "\t|" + str(wz))
        except Exception as err:
            pass
    isdo = input("查票完成，请输入1继续…")
    # isdo=1
    if isdo == 1 or isdo == "1":
        pass
    else:
        raise Exception("输入不是1，结束执行")


def url_open(url, data=None):
    req = urllib.request.Request(url, data)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
    req_data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return req_data


def login(user, passwd):
    # 以下进行登陆操作
    print("Cookie处理中…")
    # 建立cookie处理
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    urllib.request.install_opener(opener)
    # 以下进入自动登录部分
    loginurl = "https://kyfw.12306.cn/otn/login/init#"
    req0data = url_open(loginurl)

    yzmurl = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"
    while True:
        urllib.request.urlretrieve(yzmurl, "./12306_yzm.png")
        yzm = input("请输入验证码，输入第几张图片即可")
        if yzm != "re":
            break

    # x坐标(35,112,173,253)，y坐标(45)
    # x坐标(35,112,173,253)，y坐标(114)
    def getxy(pic):
        if pic == 1:
            xy = ['35', '45']
        if pic == 2:
            xy = ['112', '45']
        if pic == 3:
            xy = ['173', '45']
        if pic == 4:
            xy = ['253', '45']
        if pic == 5:
            xy = ['35', '114']
        if pic == 6:
            xy = ['112', '114']
        if pic == 7:
            xy = ['173', '114']
        if pic == 8:
            xy = ['253', '114']
        return xy

    allpicpos = []
    for i in yzm:
        thisxy = getxy(int(i))
        allpicpos.extend(thisxy)
    allpicpos2 = ','.join(allpicpos)
    # print(allpicpos2)
    # post验证码验证
    yzmposturl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    yzmpostdata = urllib.parse.urlencode({
        "answer": allpicpos2,
        "rand": "sjrand",
        "login_site": "E",
    }).encode('utf-8')
    req1data = url_open(yzmposturl, yzmpostdata)
    # post账号密码验证
    loginposturl = "https://kyfw.12306.cn/passport/web/login"
    loginpostdata = urllib.parse.urlencode({
        "username": user,
        "password": passwd,
        "appid": "otn",
    }).encode('utf-8')
    req2data = url_open(loginposturl, loginpostdata)
    # 其他验证
    loginposturl2 = "https://kyfw.12306.cn/otn/login/userLogin"
    loginpostdata2 = urllib.parse.urlencode({
        "_json_att": "",
    }).encode('utf-8')
    req2data_2 = url_open(loginposturl2, loginpostdata2)

    loginposturl3 = "https://kyfw.12306.cn/passport/web/auth/uamtk"
    loginpostdata3 = urllib.parse.urlencode({
        "appid": "otn",
    }).encode('utf-8')
    req2data_3 = pq(url_open(loginposturl3, loginpostdata3))
    # pat_req2='"newapptk":"(.*?)"'
    # tk=re.compile(pat_req2,re.S).findall(req2data_3)[0]
    tk = json.loads(req2data_3('p').text())['newapptk']

    loginposturl4 = "https://kyfw.12306.cn/otn/uamauthclient"
    loginpostdata4 = urllib.parse.urlencode({
        "tk": tk,
    }).encode('utf-8')
    req2data_4 = url_open(loginposturl4, loginpostdata4)
    print(req2data_4)
    # 爬个人中心页面
    centerurl = "https://kyfw.12306.cn/otn/index/initMy12306"
    req3data = url_open(centerurl)
    # print(req3data)
    print("登陆完成")


def booking(date, start, to, student):
    # isdo="1"
    isdo = input("如果需要订票，请输入1继续，否则请输入其他数据")
    if isdo == 1 or isdo == "1":
        pass
    else:
        raise Exception("输入不是1，结束执行")
    thiscode = input("请输入要预定的车次：")
    chooseno = "None"
    # chooseno="1"
    while True:
        try:
            # 订票
            # 先初始化一下订票界面
            initurl = "https://kyfw.12306.cn/otn/leftTicket/init"
            initdata = url_open(initurl)
            # 再爬对应订票信息
            bookurl = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + start + "&leftTicketDTO.to_station=" + to + "&purpose_codes=" + student
            data = pq(bookurl)('p').text()
            req4data = json.loads(data)
            # 存储车次与secretStr信息
            allcheci = req4data['data']['result']
            checimap = req4data['data']['map']
            code = []
            secretStr = []
            zy = []
            for item in allcheci:
                try:
                    thischeci = item.split("|")
                    # print(thischeci)
                    # [3]---code
                    thiscode1 = thischeci[3]
                    code.append(thiscode1)
                    # [0]---secretStr
                    secretStr.append(thischeci[0].replace('"', ""))
                    # [31]-zy
                    thiszy = thischeci[31]
                    zy.append(thiszy)
                except Exception as err:
                    pass
            # 用字典trainzy存储车次有没有票的信息
            trainzy = dict(zip(code, zy))

            # 用字典traindata存储车次secretStr信息，以供后续订票操作
            # 存储的格式是：traindata={"车次1":secretStr1,"车次2":secretStr2,…}
            traindata = dict(zip(code, secretStr))
            # 订票-第1次post-主要进行确认用户状态
            checkurl = "https://kyfw.12306.cn/otn/login/checkUser"
            checkdata = urllib.parse.urlencode({
                "_json_att": ""
            }).encode('utf-8')
            req5data = url_open(checkurl, checkdata)
            # 自动得到当前时间并转为年-月-格式，因为后面请求数据需要用到当前时间作为返程时间backdate
            backdate = datetime.datetime.now()
            backdate = backdate.strftime("%Y-%m-%d")
            # 订票-第2次post-主要进行“预订”提交
            submiturl = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
            submitdata = urllib.parse.urlencode({
                "secretStr": traindata[thiscode],
                "train_date": date,
                "back_train_date": backdate,
                "tour_flag": "dc",
                "purpose_codes": student,
                "query_from_station_name": start1,
                "query_to_station_name": to1,
            })
            submitdata2 = submitdata.replace("%25", "%")
            submitdata3 = submitdata2.encode('utf-8')
            req6data = url_open(submiturl, submitdata3)
            # 订票-第3次post-主要获取Token、leftTicketStr、key_check_isChange、train_location
            initdcurl = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
            initdcdata = urllib.parse.urlencode({
                "_json_att": ""
            }).encode('utf-8')
            req7data = url_open(initdcurl, initdcdata)
            # 获取train_no、leftTicketStr、fromStationTelecode、toStationTelecode、train_location
            # print(req7data)
            train_no_pat = "'train_no':'(.*?)'"
            leftTicketStr_pat = "'leftTicketStr':'(.*?)'"
            fromStationTelecode_pat = "from_station_telecode':'(.*?)'"
            toStationTelecode_pat = "'to_station_telecode':'(.*?)'"
            train_location_pat = "'train_location':'(.*?)'"
            pattoken = "var globalRepeatSubmitToken.*?'(.*?)'"
            patkey = "'key_check_isChange':'(.*?)'"
            train_no_all = re.compile(train_no_pat).findall(req7data)
            if (len(train_no_all) != 0):
                train_no = train_no_all[0]
            else:
                raise Exception("train_no获取失败")
            leftTicketStr_all = re.compile(leftTicketStr_pat).findall(req7data)
            if (len(leftTicketStr_all) != 0):
                leftTicketStr = leftTicketStr_all[0]
            else:
                raise Exception("leftTicketStr获取失败")
            fromStationTelecode_all = re.compile(fromStationTelecode_pat).findall(req7data)
            if (len(fromStationTelecode_all) != 0):
                fromStationTelecode = fromStationTelecode_all[0]
            else:
                raise Exception("fromStationTelecod获取失败")
            toStationTelecode_all = re.compile(toStationTelecode_pat).findall(req7data)
            if (len(toStationTelecode_all) != 0):
                toStationTelecode = toStationTelecode_all[0]
            else:
                raise Exception("toStationTelecode获取失败")
            train_location_all = re.compile(train_location_pat).findall(req7data)
            if (len(train_location_all) != 0):
                train_location = train_location_all[0]
            else:
                raise Exception("train_location获取失败")
            tokenall = re.compile(pattoken).findall(req7data)
            if (len(tokenall) != 0):
                token = tokenall[0]
            else:
                raise Exception("Token获取失败")
            keyall = re.compile(patkey).findall(req7data)
            if (len(keyall) != 0):
                key = keyall[0]
            else:
                raise Exception("key_check_isChange获取失败")
            # 还需要获取train_location
            pattrain_location = "'tour_flag':'dc','train_location':'(.*?)'"
            train_locationall = re.compile(pattrain_location).findall(req7data)
            if (len(train_locationall) != 0):
                train_location = train_locationall[0]
            else:
                raise Exception("train_location获取失败")
            # 自动post网址4-获取乘客信息
            getuserurl = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
            getuserdata = urllib.parse.urlencode({
                "REPEAT_SUBMIT_TOKEN": token,
            }).encode('utf-8')
            req8data = url_open(getuserurl, getuserdata)
            # 获取用户信息
            # 提取姓名
            namepat = '"passenger_name":"(.*?)"'
            # 提取身份证
            idpat = '"passenger_id_no":"(.*?)"'
            # 提取手机号
            mobilepat = '"mobile_no":"(.*?)"'
            # 提取对应乘客所在的国家
            countrypat = '"country_code":"(.*?)"'
            nameall = re.compile(namepat).findall(req8data)
            idall = re.compile(idpat).findall(req8data)
            mobileall = re.compile(mobilepat).findall(req8data)
            countryall = re.compile(countrypat).findall(req8data)
            # 选择乘客
            if chooseno != "None":
                pass
            else:
                # 输出乘客信息，由于可能有多位乘客，所以通过循环输出
                for i in range(0, len(nameall)):
                    print("第" + str(i + 1) + "位用户,姓名:" + str(nameall[i]))
                chooseno = input("请选择要订票的用户的序号，此处只能选择一位哦，如需选择多\
    位，可以自行修改一下代码")
                # thisno为对应乘客的下标，比序号少1，比如序号为1的乘客在列表中的下标为0
                thisno = int(chooseno) - 1
            if (trainzy[thiscode] == "无"):
                print("当前无票，继续监控…")
                continue
            # 总请求1-点击提交后步骤1-确认订单(在此只定二等座，座位类型为1，如需选择多种类型座位，可
            # 以自行修改一下代码使用if判断一下即可)
            checkOrderurl = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
            checkdata = urllib.parse.urlencode({
                "cancel_flag": 2,
                "bed_level_order_num": "000000000000000000000000000000",
                "passengerTicketStr": "M,0,1," + str(nameall[thisno]) + ",1," + str(idall[thisno]) + ",\
    " + str(mobileall[thisno]) + ",N",
                "oldPassengerStr": str(nameall[thisno]) + ",1," + str(idall[thisno]) + ",1_",
                "tour_flag": "dc",
                "randCode": "",
                "whatsSelect": 1,
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token,
            }).encode('utf-8')
            req9data = url_open(checkOrderurl, checkdata)
            print("确认订单完成，即将进行下一步")
            # 总请求2-点击提交后步骤2-获取队列
            getqueurl = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
            # checkdata=checkOrderdata.encode('utf-8')
            # 将日期转为格林时间
            # 先将字符串转为常规时间格式
            thisdatestr = date  # 需要的买票时间
            thisdate = datetime.datetime.strptime(thisdatestr, "%Y-%m-%d").date()
            # 再转为对应的格林时间
            gmt = '%a+%b+%d+%Y'
            thisgmtdate = thisdate.strftime(gmt)
            # 将leftstr2转成指定格式
            leftstr2 = leftTicketStr.replace("%", "%25")
            getquedata = "train_date=" + str(thisgmtdate) + "+00%3A00%3A00+GMT%2B0800&train_no=" + train_no + "&sta\
    tionTrainCode=" + thiscode + "&seatType=M&fromStationTelecode=" + fromStationTelecode + "&toStationTelecod\
    e=" + toStationTelecode + "&leftTicket=" + leftstr2 + "&purpose_codes=00&train_location=" + train_location + "&_j\
    son_att=&REPEAT_SUBMIT_TOKEN=" + str(token)
            getdata = getquedata.encode('utf-8')
            req10data = url_open(getqueurl, getdata)
            print("获取订单队列完成，即将进行下一步")
            # 总请求3-确认步骤1-配置确认提交
            confurl = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
            confdata2 = urllib.parse.urlencode({
                "passengerTicketStr": "M,0,1," + str(nameall[thisno]) + ",1," + str(idall[thisno]) + ",\
    " + str(mobileall[thisno]) + ",N",
                "oldPassengerStr": str(nameall[thisno]) + ",1," + str(idall[thisno]) + ",1_",
                "randCode": "",
                "purpose_codes": "00",
                "key_check_isChange": key,
                "leftTicketStr": leftTicketStr,
                "train_location": train_location,
                "choose_seats": "",
                "seatDetailType": "000",
                "whatsSelect": "1",
                "roomType": "00",
                "dwAll": "N",
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token,
            }).encode('utf-8')
            req11data = url_open(confurl, confdata2)
            print("配置确认提交完成，即将进行下一步")
            time1 = time.time()
            while True:
                # 总请求4-确认步骤2-获取orderid
                time2 = time.time()
                if ((time2 - time1) // 60 > 5):
                    print("获取orderid超时，正在进行新一次抢购")
                    break
                getorderidurl = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=" + str(
                    int(time.time() * 1000)) + "&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=" + str(token)
                req12data = url_open(getorderidurl)
                patorderid = '"orderId":"(.*?)"'
                orderidall = re.compile(patorderid).findall(req12data)
                if len(orderidall) == 0:
                    print("未获取到orderid，正在进行新一次的请求。")
                    continue
                else:
                    orderid = orderidall[0]
                    break
            print("获取orderid完成，即将进行下一步")
            # 总请求5-确认步骤3-请求结果
            resulturl = "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
            resultdata = "orderSequence_no=" + orderid + "&_json_att=&REPEAT_SUBMIT_TOKEN=" + str(token)
            resultdata2 = resultdata.encode('utf-8')
            req13data = url_open(resulturl, resultdata2)
            print("请求结果完成，即将进行下一步")
            try:
                # 总请求6-确认步骤4-支付接口页面
                payurl = "https://kyfw.12306.cn/otn//payOrder/init"
                paydata = "_json_att=&REPEAT_SUBMIT_TOKEN=" + str(token)
                paydata2 = paydata.encode('utf-8')
                req14data = url_open(payurl, paydata2)
                print("订单已经完成提交，您可以登录后台进行支付了。")
                break
            except Exception as err:
                break
        except Exception as err:
            print(err)


if __name__ == '__main__':
    # 为了防止ssl出现问题，你可以加上下面一行代码
    ssl._create_default_https_context = ssl._create_unverified_context
    # 查票
    # 常用三字码与站点对应关系
    #areatocode = {"上海": "SHH", "北京": "BJP", "南京": "NJH", "昆山": "KSH", "杭州": "HZH", "桂林": "GLZ"}
    areatocode = get_site_abb()
    start1=input("请输入起始站:")
    #start1 = "北京"
    start = areatocode[start1]
    to1=input("请输入到站:")
    #to1 = "上海"
    to = areatocode[to1]
    # isstudent=input("是学生吗？是：1，不是：0")
    isstudent = "0"
    date=input("请输入要查询的乘车开始日期的年月，如2017-03-05：")
    #date = "2018-09-01"
    if isstudent == "0":
        student = "ADULT"
    else:
        student = "0X00"
    context = ssl._create_unverified_context()
    check_ticks(date, start, to, student)
    login(myuser, mypasswd)
    booking(date, start, to, student)
