import re,requests,os,json
def get_station():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9114"
    res = requests.get(url,verify=True)
    starts = re.findall("([\u4e00-\u9fa5]+)\|([A-Z]+)",res.text)
    starts = dict(starts)
    starts = str(starts)
    write(starts,"staions.txt")
def write(x,y):
    l = open(y,"w",encoding="utf-8")
    l.write(x)
    l.close()
def read(y):
    file = open(y,"r",encoding="utf-8")
    data = file.readline()
    file.close()
    return data
"""判断是否存在该文件"""
def is_starts(y):
    is_starts = os.path.exists(y)
    return is_starts
"""下载出发时间"""
def Time():
    url = "https://www.12306.cn/index/script/core/common/qss_v10042.js"
    res = requests.get(url,verify=True)
    json_str = re.findall("{[^}]+}",res.text)
    time_js = json.loads(json_str[0])
    time_js = str(time_js)
    write(time_js,"time.txt")
    return time_js
data = []#整理好的车次信息
type_data = []#用于保存车次分类后的信息
def query(date,from_station,to_station):
    data.clear()
    type_data.clear()
    heards = {
        "Referer":f"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E7%9F%B3%E5%AE%B6%E5%BA%84,{from_station}&ts=%E5%8C%97%E4%BA%AC,{to_station}&date={date}&flag=N,N,Y",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36",
        "Cookie":"JSESSIONID=6420858B27361F20F2A7E24BE12366DC; _jc_save_wfdc_flag=dc; BIGipServerotn=300941834.24610.0000; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromStation=%u77F3%u5BB6%u5E84%2CSJP; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_fromDate=2019-10-21; _jc_save_toDate=2019-10-21; RAIL_EXPIRATION=1571948179246; RAIL_DEVICEID=R_r5VfnYv8oexGskPEtcBgGOz0s5Emz5S02MUTNG336_GD8HpTs2ldPdpoaCXDadzdDIbj2yCXIk_zRTd1CwJCDSBnVpIaQA2yunMVFMblUcZPKm36iQNtWHnEF-Ty0_1M1t2pfpQfTiv_HSEG58iFHaG0tiLhDa",
    }
    url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT"
    res = requests.get(url,headers=heards)
    print(url)
    print(res.text)
    result = res.json()
    result = result["data"]["result"]
    # 判断车站是否存在
    if is_starts("staions.txt") == True:
        print("2")
        stations = eval(read("staions.txt"))
        if len(result) != 0:
            n = 0
            for i in result:
                tmp_list = i.split("|")
                from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
                to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
                seat = [tmp_list[3],from_station,to_station,tmp_list[8],tmp_list[9],tmp_list[10],tmp_list[32],tmp_list[31],tmp_list[30],tmp_list[21],tmp_list[23],tmp_list[33],tmp_list[28],Time()[24],tmp_list[29],tmp_list[26]]
                newSeat = []
                for s in seat:
                    if s == "":
                        s = "---"
                    else:
                        s = s
                    newSeat.append(s)
                data.append(newSeat)
                print(data[n])
                n+=1
            return data
def g_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith("G")   #判断车次首字母
            if i:  #如果是将该信息添加到高铁数据中
                type_data.append(g)
#移出高铁信息方法
def r_g_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for g in data:
            i = g[0].startswith("G")
            if i:
                type_data.remove(g)
def d_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith("D")   #判断车次首字母
            if i:  #如果是将该信息添加到高铁数据中
                type_data.append(g)
def r_d_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for g in data:
            i = g[0].startswith("D")
            if i:
                type_data.remove(g)
def z_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith("Z")   #判断车次首字母
            if i:  #如果是将该信息添加到高铁数据中
                type_data.append(g)
def r_z_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for g in data:
            i = g[0].startswith("Z")
            if i:
                type_data.remove(g)
def t_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith("T")   #判断车次首字母
            if i:  #如果是将该信息添加到高铁数据中
                type_data.append(g)
def r_t_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for g in data:
            i = g[0].startswith("T")
            if i:
                type_data.remove(g)
def k_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith("K")   #判断车次首字母
            if i:  #如果是将该信息添加到高铁数据中
                type_data.append(g)
def r_k_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for g in data:
            i = g[0].startswith("K")
            if i:
                type_data.remove(g)
# print(query("2019-10-21","SJP","BJP"))
today_car_list = []#保存今天列车信息，已经处理是否有票
three_car_list = []#保存三天列车信息，已经处理是否有票
five_car_list = []#保存五天列车信息，已经处理是否有票
today_list = []#保存今天列车信息，未处理是否有票
three_list = []#保存三天列车信息，未处理是否有票
five_list = []#保存五天，未处理是否有票
"""判断高级软卧，软卧，硬卧是否有票"""
def is_ticket(tmp_list,from_station,to_station):
    if tmp_list[21] == "有" or tmp_list[23] == "有" or tmp_list[28] == "有":
        tmp_tem = "有"
    else:
        if tmp_list[21].isdigit() or tmp_list[23].isdigit() or tmp_list[28].isdigit():
            tmp_tem = "有"
        else:
            tmp_tem = "无"
    #创建新的坐标列表,显示是否有卧铺车票
    new_seat = [tmp_list[3],from_station,to_station,tmp_list[8],tmp_list[9],tmp_list[10],tmp_tem]
    return new_seat
"""查询卧铺票数据分析"""
def query_ticketiong_analysis(date,from_station,to_station,which_day):
    heards = {
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E7%9F%B3%E5%AE%B6%E5%BA%84,SJP&date=2019-10-12&flag=N,N,Y",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36",
        "Cookie": "JSESSIONID=65EDDCA1623C94E1A1E8C3E89FC34B9C; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u77F3%u5BB6%u5E84%2CSJP; RAIL_EXPIRATION=1571041916586; RAIL_DEVICEID=mn_mqZk69ffyr1BC-GeoD71aJL_IOWWngRCYC-lVvlGNtdi60qYFaphX9ZHSO7Xn-whzA8YbqY2FBvdxfxAC3vnVFPQHJCMt_gVf2aKAumZFg2ch5kSTMgc9oIyEwyXGKoRKbQESfFMOesh_HjChXodTmlYHgIQ8; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2019-10-12; _jc_save_toDate=2019-10-12; BIGipServerpool_passport=250413578.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=1324352010.38945.0000",
    }
    url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT"
    res = requests.get(url, headers=heards)
    result = res.json()
    result = result["data"]["result"]
    # 判断车站是否存在
    if is_starts("staions.txt") == True:
        stations = eval(read("staions.txt"))
        if len(result) != 0:
            for i in result:
                tmp_list = i.split("|")
                from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
                to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
                #创建座位数组,其中包含高级软卧，软卧，硬卧的信息
                seat = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10], tmp_list[21], tmp_list[23],tmp_list[28]]
                #判断今天的车次信息
                if which_day == 1:
                    #将高铁、动车、c开头的车次排序
                    if seat[0].startwith("G") == False and seat[0].startwith("D") == False and seat[0].startwith("c") == False:
                        #将高级软卧，软卧，硬卧未处理信息添加至列表中
                        today_list.append(seat)
                        #判断某车次是否有票
                        new_seat = is_ticket(tmp_list,from_station,to_station)
                        #将判断后的车次信息添加至对应的列表中
                        today_car_list.append(new_seat)
                if which_day == 3:
                    #将高铁、动车、c开头的车次排序
                    if seat[0].startwith("G") == False and seat[0].startwith("D") == False and seat[0].startwith("c") == False:
                        #将高级软卧，软卧，硬卧未处理信息添加至列表中
                        three_list.append(seat)
                        #判断某车次是否有票
                        new_seat = is_ticket(tmp_list,from_station,to_station)
                        #将判断后的车次信息添加至对应的列表中
                        three_car_list.append(new_seat)
                if which_day == 5:
                    #将高铁、动车、c开头的车次排序
                    if seat[0].startwith("G") == False and seat[0].startwith("D") == False and seat[0].startwith("c") == False:
                        #将高级软卧，软卧，硬卧未处理信息添加至列表中
                        five_list.append(seat)
                        #判断某车次是否有票
                        new_seat = is_ticket(tmp_list,from_station,to_station)
                        #将判断后的车次信息添加至对应的列表中
                        five_car_list.append(new_seat)
"""查询起售时间"""
station_name_list = []
station_time_list = []
def query_time(station):
    station_name_list.clear()
    station_time_list.clear()
    stations = eval(read("time.txt"))
    url = "https://www.12306.cn/index/otn/index12306/queryScSname"
    form_data = {"station_titlecode":station}
    response = requests.post(url,data=form_data,verify=True)
    response.encoding = "utf-8"
    json_data = json.loads(response.text)
    data = json_data.get("data")
    for i in data:
        if i in stations:
            station_name_list.append(i)
    for name in station_name_list:
        time = stations.get(name)
        station_time_list.append(time)
    return station_name_list,station_time_list



