#!C:\\Python3.6\\python.exe
# encoding:utf-8
# Authored by Cless Li, at 2019-9-19

def calculat(quota: float, percentage):
    return quota * (float(percentage) / 100.0)


if __name__ == '__main__':
    income = ''
    while not isinstance(income, float):
        try:
            income = float(input('请输入当前月收入（货币类型：￥）\n').replace(',',''))
        except Exception as err:
            print('请输入正确的金额格式，如：5500.50或者6000')
            income = ''

    housing_per = 31
    traffic_per = 6
    health_per = 5
    food_per = 22
    learn_per = 2
    other_per = 9
    save_per = 25

    print('住房：%s' % calculat(income, housing_per))
    print('交通：%s' % calculat(income, traffic_per))
    print('健康：%s' % calculat(income, health_per))
    print('饮食：%s' % calculat(income, food_per))
    print('学习：%s' % calculat(income, learn_per))
    print('其他：%s' % calculat(income, other_per))
    print('存储：%s' % calculat(income, save_per))

    end = 'no'
    while end != 'yes':
        end = input("记录完毕，请输入'yes': ")
