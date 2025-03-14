from selenium.webdriver.common.by import By
from lib.webui_smp import smp_ui
import pytest
from time import sleep
from cfg import *

pytestmark = [pytest.mark.网页测试, pytest.mark.业务规则]


@pytest.fixture(scope='module')
def into_service_rule_mgr():
    smp_ui.driver.get(SMP_URL_SERVICE_RULE)
    sleep(1)
    yield


@pytest.fixture(scope='function')
def del_newly_added_service_rule():
    yield
    print('删除添加的设备')
    smp_ui.del_newly_added_item()


def test_smp_service_rule_001(into_service_rule_mgr, del_newly_added_service_rule):
    smp_ui.add_service_rule(rule_name='全国-电瓶车充电费率1', rule_type='预付费-下发业务量', rule_desc='全国-电瓶车充电费率1描述', min_price='0.1',
                            expected_price='2', charge_unit='千瓦时', unit_price='1')
    service_rules = smp_ui.list_all_rules('预付费-下发业务量')
    assert service_rules == [[
        '全国-电瓶车充电费率1',
        '预付费-下发业务量',
        '0.1',
        '2',
        '千瓦时',
        '1',
        '全国-电瓶车充电费率1描述'
    ]]


def test_smp_service_rule_101(into_service_rule_mgr, del_newly_added_service_rule):
    smp_ui.add_service_rule(rule_name='南京-洗车机费率1', rule_type='预付费-下发费用', rule_desc='南京-洗车机费率1描述', min_price='2',
                            expected_price='10')
    service_rules = smp_ui.list_all_rules('预付费-下发费用')
    assert service_rules == [[
        '南京-洗车机费率1',
        '预付费-下发费用',
        '2',
        '10',
        '南京-洗车机费率1描述'
    ]]


def test_smp_service_rule_201(into_service_rule_mgr, del_newly_added_service_rule):
    smp_ui.add_service_rule('南京-存储柜费率1', '后付费-上报业务量', '南京-存储柜费率1描述',
                            fee_rate_list=[['100L', '小时', '2'], ['50L', '小时', '1'], ['10L', '小时', '0.5']])
    service_rules = smp_ui.list_all_rules('后付费-上报业务量')
    assert service_rules == [[
        '南京-存储柜费率1',
        '后付费-上报业务量',
        [['100L', '小时', '2'], ['50L', '小时', '1'], ['10L', '小时', '0.5']],
        '南京-存储柜费率1描述']]
