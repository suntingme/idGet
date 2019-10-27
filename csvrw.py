# -*- coding: utf-8 -*-


import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def csv_write(path, data):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        for row in data:
            writer.writerow(row)
    return True


def csv_write_dict(path,data,headers=['title','publishtime','place','workyear','org','education','number','description','requirement']):
    # if not os.path.exists(path):
    #     f = open(path,'w')
    #     f.close()
    # 标题存在则追加，不存在则写入标题
    with open(path, "a")as f:
        f_csv = csv.DictWriter(f, headers)
        # 以读的方式打开csv 用csv.reader方式判断是否存在标题。
        with open(path, "r") as fr:
            reader = csv.reader(fr)
            if not [row for row in reader]:
                f_csv.writeheader()
                f_csv.writerows(data)
            else:
                f_csv.writerows(data)
    return True

