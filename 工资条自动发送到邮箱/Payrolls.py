# encoding:utf-8

import xlrd
import json
import re


class Payrolls(object):
    def __init__(self, excel_fp, level):
        self.excel_fp = excel_fp
        self.excel = {}
        self.sheet_len = {}
        self.payrolls = {}
        self.title_level = level
        self.init_payrolls()
        self.payrolls_list = []
        self.format_payrolls()

    def get_list(self, data):
        if isinstance(data, dict):
            for key in data:
                return self.get_list(data.get(key))
        elif isinstance(data, list):
            return data
        else:
            return data

    def get_title(self, sheet_name, level=1, tmp=None):
        if tmp is None:
            tmp = []
            for l in range(self.title_level):
                tmp.append('')
        if level <= self.title_level:
            for mark in range(self.sheet_len.get(sheet_name)):
                for x, y in self.excel.get(sheet_name).get(level):
                    if x == mark + 1:
                        colspan = y - x + 1
                        rowspan = self._get_rowspan(sheet_name, x, y, level)
                        if rowspan:
                            value = self.excel.get(sheet_name).get(level).get((x, y))
                            tmp[level - 1] += '\t\t<td rowspan = "%s" colspan = "%s">%s</td>\n' % (
                            str(rowspan), str(colspan), value)
            return self.get_title(sheet_name, level + 1, tmp)
        else:
            title = ''
            for item in tmp:
                title += '\t<tr>\n%s\t</tr>\n' % item
            return title

    def _get_rowspan(self, sheet, x, y, level, rowspan=1):
        if isinstance(self.excel.get(sheet).get(level - 1), dict) and (self.excel.get(sheet).get(level - 1).get((x, y)) == self.excel.get(sheet).get(level).get((x, y)) and rowspan == 1):
            return None
        else:
            if self.excel.get(sheet).get(level + 1).get((x, y)) == self.excel.get(sheet).get(level).get((x, y)):
                rowspan += 1
                return self._get_rowspan(sheet, x, y, level + 1, rowspan)
            else:
                return rowspan

    def get_payroll(self, sheet_name, title, level, tmp=None):
        if tmp is None:
            tmp = []
        if self.excel.get(sheet_name).get(level):
            payroll = '<table border = "1">\n%s\t<tr>\n' % title
            for mark in range(self.sheet_len.get(sheet_name)):
                for x, y in self.excel.get(sheet_name).get(level):
                    if mark + 1 == x:
                        value = self.excel.get(sheet_name).get(level).get((x, y))
                        payroll += '\t\t<td>%s</td>\n' % value
            payroll += '\t</tr>\n</table>'
            tmp.append(payroll)
            return self.get_payroll(sheet_name, title, level + 1, tmp)
        else:
            return tmp

    def format_payrolls(self):
        mail_match = r'^.*邮箱.*|^.*e[-_]?mail.*|^.*mail.*'
        for sheet in self.payrolls:
            for key in self.payrolls.get(sheet):
                if re.match(mail_match, key):
                    mail_list = self.get_list(self.payrolls.get(sheet).get(key))
                    break
                else:
                    mail_list = []
            title = self.get_title(sheet)
            payroll_list = self.get_payroll(sheet, title, self.title_level + 1)
            if mail_list:
                for n in range(len(mail_list)):
                    self.payrolls_list.append({'mail_address': mail_list[n], 'context': payroll_list[n]})

    def init_payrolls(self):
        for sheet in self.excel_fp.sheet_names():
            if self.excel_fp.sheet_by_name(sheet).nrows:
                self.sheet_len.update({sheet: self.excel_fp.sheet_by_name(sheet).row_len(0)})
                sheet_info = self.sheet_parse(sheet)
            else:
                sheet_info = None
            if sheet_info:
                # self.excel.update({sheet: self.excel_fp.sheet_by_name(sheet)})
                self.excel.update({sheet: sheet_info})
                # print(self.excel)
                # print(self.payrolls)
                self.payrolls.update({sheet: self.payroll_parse(sheet)})

    def sheet_parse(self, sheet_name):
        sheet_dict = {}
        sheet_info = self.excel_fp.sheet_by_name(sheet_name)
        merge_dict = self.merged_cell(sheet_info)
        # print(merge_dict)
        sheet_dict.update(self.load_cell(sheet_info, merge_dict))
        return sheet_dict

    def load_cell(self, sheet, merge):
        lines = sheet.nrows
        cells_dict = {}
        for line in range(lines):
            line += 1
            cells_dict.update({line: {}})
            merge_cell = merge.get(line)
            merge_cell_flag = []
            if merge_cell:
                cells_dict[line].update(merge_cell)
                for x, y in merge_cell:
                    if x != y:
                        for flag in range(x, y):
                            merge_cell_flag.append(flag)
                    else:
                        merge_cell_flag.append(x)
            rows = sheet.row_len(line - 1)
            line_values = sheet.row_values(line - 1)
            for row in range(rows):
                if ((row + 1) not in merge_cell_flag and line <= self.title_level and line_values[row]) or line > self.title_level:
                    # print("line: %s, x: %s, y: %s, value: %s" % (line, row + 1, row + 1, line_values[row]))
                    cells_dict[line].update({(row + 1, row + 1): line_values[row]})
        # print(cells_dict)
        return cells_dict

    def merged_cell(self, sheet):
        merge_dict = {}
        for level in range(self.title_level):
            merge_dict[level + 1] = {}
        merge_cells = sheet.merged_cells
        # print(merge_cells)
        for (llow, lhigh, rlow, rhigh) in merge_cells:
            value_mg_cell = sheet.cell_value(llow, rlow)
            if min(lhigh, self.title_level) > (llow + 1) and llow < self.title_level:
                for level in range(min(lhigh, self.title_level)):
                    merge_dict[level + 1].update({(rlow + 1, rhigh): value_mg_cell})
                    # print(merge_dict)
            elif min(lhigh, self.title_level) == (llow + 1) and self.title_level > llow:
                # print(llow, lhigh, rlow, rhigh)
                # print(value_mg_cell)
                # print("level: %s, x: %s, y: %s" % (llow + 1, rlow + 1, rhigh))
                merge_dict[(llow + 1)].update({(rlow + 1, rhigh): value_mg_cell})
        return merge_dict

    def payroll_parse(self, sheet, line=1, fx=None, fy=None, tmp_dict=None, tmp_payroll=None):
        if tmp_payroll is None:
            tmp_payroll = []
        if tmp_dict is None:
            tmp_dict = {}
        if self.title_level > line > 0:
            if line == 1:
                for x, y in self.excel.get(sheet).get(line):
                    tmp_dict.update(
                        {self.excel.get(sheet).get(line).get((x, y)): self.payroll_parse(sheet,
                                                                                         line + 1,
                                                                                         x,
                                                                                         y)
                         }
                    )
            elif line > 1:
                for x, y in self.excel.get(sheet).get(line):
                    if fx <= x <= fy:
                        tmp_dict.update(
                            {self.excel.get(sheet).get(line).get((x, y)): self.payroll_parse(sheet,
                                                                                             line + 1,
                                                                                             x,
                                                                                             y)
                             }
                        )
        elif line == self.title_level:
            for x, y in self.excel.get(sheet).get(line):
                if fx <= x <= fy:
                    # print(tmp_dict)
                    tmp_dict.update({self.excel.get(sheet).get(line).get((x, y)): self.payroll_parse(sheet,
                                                                                                     line + 1,
                                                                                                     x,
                                                                                                     y)
                                     }
                                    )
                    # print(tmp_dict)
        elif line > self.title_level > 0:
            if self.excel.get(sheet).get(line):
                for x, y in self.excel.get(sheet).get(line):
                    if fx <= x <= fy:
                        tmp_payroll.append(self.excel.get(sheet).get(line).get((x, y)))
                        # print(tmp_payroll, x, y, fx, fy)
                        return self.payroll_parse(sheet, line + 1, fx, fy, tmp_payroll=tmp_payroll)
            else:
                # print(tmp_payroll)
                return tmp_payroll
        return tmp_dict


if __name__ == '__main__':
    title_level = 2
    with xlrd.open_workbook(r'工资条1.xlsx') as workbook:
        # print(workbook.sheet_by_name('Sheet2').nrows)
        payrolls = Payrolls(workbook, title_level)
        print(payrolls.payrolls_list)
