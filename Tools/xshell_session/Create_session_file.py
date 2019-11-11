# encoding:utf-8
import xlrd, os ,re
with xlrd.open_workbook('.\主机信息.xlsx') as data:
    sheets_names = data.sheet_names()
#print(sheets_names)
def mkdir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print('[%s]目录已存在。' % (path))
    except Exception as err:
        print('创建目录失败： \n[%s]' % (err))
        exit()


def create_xsh(new_file_path, host_ip, defualt_file='.\\test.txt'):
    with open(defualt_file, 'r') as old_fp:
        old_file = old_fp.read()
        #print(old_file)
        new_file = re.sub(r'Host=', 'Host=' + host_ip, old_file)
        #print(new_file)
        with open(new_file_path, 'w') as new_fp:
            new_fp.write(new_file)
        #exit()


if __name__ == '__main__':
    for sheet in sheets_names:
        table = data.sheet_by_name(sheet)
        list1 = table.col_values(0,0,None)
        list2 = table.col_values(1,0,None)
        list3 = table.col_values(2,0,None)
        col_nums = len(list1)
        for col_num in range(0,col_nums-1):
            area = list1[col_num]
            team = list2[col_num]
            host_ip = list3[col_num]
            path = '.\\' + sheet + '\\' + area
            #print(path)
            mkdir(path)
            file_name = path + '\\' + host_ip + '-' + team + '.xsh'
            print(file_name)
            create_xsh(file_name, host_ip)
            #exit()


