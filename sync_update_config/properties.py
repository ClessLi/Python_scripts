# encoding:utf-8
# Authored by Cless Li, at 2019/08/29
# Update by Cless Li, at 2019/09/04
import chardet


def check_code(file_path):
    with open(file_path, 'rb') as f:
        cur_encoding = chardet.detect(f.read())['encoding']
        return cur_encoding


class Properties(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        self._comments_init()
        self._line_num = 0
        self._read_config()

    def _comments_init(self):
        self._comments_tmp = []

    def _read_config(self):
        with open(self.file_name, 'r', encoding=check_code(self.file_name)) as ropen:
            for line in ropen.readlines():
                self._line_num += 1
                line = line.strip()
                self.option_parse(line)

    def write_config(self):
        with open(self.file_name, 'w', encoding=check_code(self.file_name)) as wopen:
            wopen.truncate()
            wopen.seek(0)
            for key in self.properties:
                if self.properties[key].get("comments"):
                    for comments in self.properties[key].get("comments"):
                        wopen.write('#%s\n' % comments)
                wopen.write('%s = %s\n\n' % (key, self.properties[key].get("value")))

    def option_parse(self, data):
        if data.find('=') > 0 and not data.startswith('#'):
            strs = data.split('=')
            tmp_dic = {'value': strs[1].strip(), 'comments': self._comments_tmp}
            self.properties[strs[0].strip()] = tmp_dic
            self._comments_init()
        elif data.startswith('#'):
            self._comments_tmp.append(data[1:])

    def has_key(self, key):
        return key in self.properties.keys()

    def get(self, key, default_value=''):
        # if key in self.properties:
        if self.has_key(key):
            return self.properties.get(key).get('value')
        else:
            return default_value

    def set(self, key, value, comments=None):
        if self.has_key(key):
            o_value = self.properties[key]['value']
            if o_value != value:
                self.properties[key]['value'] = value
                print('The option of "%s=%s" will be updated to "%s=%s".' % (key, o_value, key, value))
            if comments:
                for comment in comments:
                    if comment not in self.properties[key]['comments']:
                        self.properties[key]['comments'].append(comment)
        else:
            self.properties[key] = {'value': value, 'comments': comments}
            print('The option of "%s=%s" will be appended.' % (key, value))

    def remove(self, key):
        if self.has_key(key):
            self.properties.pop(key)
            print('The option of "%s" will be removed.' % key)


if __name__ == '__main__':
    file_path = 'test.properties'
    props = Properties(file_path)  # 读取文件
    props.set('key_a', 'value_a')  # 修改/添加key=value
    print(props.get('key_a'))  # 根据key读取value
    print("props.has_key('key_a')=" + str(props.has_key('key_a')))  # 判断是否包含该key
