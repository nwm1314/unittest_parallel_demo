import datetime
import multiprocessing
import os
import sys
import unittest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from tools.GenerateHtmlReport import GenerateHtmlReport
from tools.HTMLTestRunner import HTMLTestRunner


def sortResult(result_list, cls_list, rmap_list):
    rmap = {}
    classes = []
    for n,t,o,e in result_list:
        cls = t.__class__
        if not cls in rmap:
            rmap[cls] = []
            classes.append(cls)
        rmap[cls].append((n,t,o,e))
    for cls in classes:
        cls_list.append(cls)
        rmap_list.append(rmap[cls])


def do(suit, count_list, cls_list, rmap_list, path):
    fp = open(path, 'wb')
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='子进程测试报告', description='用例执行情况')  # 定义测试报告
    res = runner.run(suit)
    sortResult(res.result, cls_list, rmap_list)
    count_list[0] += res.success_count
    count_list[1] += res.failure_count
    count_list[2] += res.error_count
    fp.close()


if __name__ == '__main__':
    manage = multiprocessing.Manager()
    count_list = manage.list()
    cls_list = manage.list()
    rmap_list = manage.list()
    count_list.append(0)
    count_list.append(0)
    count_list.append(0)
    pool = multiprocessing.Pool(3)
    path = os.path.dirname(os.path.dirname(__file__))
    suites = unittest.defaultTestLoader.discover(path, 'test_*.py')
    start_time = datetime.datetime.now()
    i = 0
    for suite in suites:
        i = i + 1
        pool.apply_async(do, (suite, count_list, cls_list, rmap_list, './../test_report/report'+str(i)+'.html'))
    pool.close()
    pool.join()
    end_time = datetime.datetime.now()
    fp = open('./../test_report/report.html', 'wb')
    sort_result = list(zip(cls_list, rmap_list))
    report = GenerateHtmlReport(fp=fp, count_list=count_list, sort_result=sort_result, start_time=start_time, end_time=end_time, title="多进程汇总报告", description="用例执行情况")
    report.generateReport()
    fp.close()


