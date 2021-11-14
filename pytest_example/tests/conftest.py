# from datetime import datetime
from py.xml import html
import pytest


def pytest_html_report_title(report):
    report.title = "class Restricted"

def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Description"))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


# Excel Reporting - https://pypi.python.org/pypi/pytest-excel
# HTML Reporting - https://pypi.python.org/pypi/pytest-html
# Allure Reporting (I prefer this) - https://docs.qameta.io/allure/
# pytest ./tests --html=report.html --self-contained-html -v --excelreport=report.xls
