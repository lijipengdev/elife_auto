from selenium.webdriver.common.by import By
from lib.webui_smp import smp_ui
import pytest
from time import sleep
from cfg import *

pytestmark = [pytest.mark.网页测试, pytest.mark.设备管理]


@pytest.fixture(scope='module')
def into_service_mgr():
    smp_ui.driver.get(SMP_URL_DEVICE_MODEL)
    sleep(1)
    smp_ui.add_device_model('电瓶车充电站', 'bokpower-charger-g22-220v450w', '杭州bok 2022款450瓦 电瓶车充电站')
    smp_ui.add_device_model('洗车站', 'njcw-carwasher-g22-2s', '南京e生活2022款洗车机 2个洗车位')
    smp_ui.add_device_model('汽车充电站', 'yixun-charger-g22-220v7kw', '南京易迅能源2022款7千瓦汽车充电站')
    smp_ui.driver.get(SMP_URL_SERVICE_RULE)
    sleep(1)
    smp_ui.add_service_rule(rule_name='全国-电瓶车充电费率1', rule_type='预付费-下发业务量', rule_desc='全国-电瓶车充电费率1描述', min_price='0.1',
                            expected_price='2', charge_unit='千瓦时', unit_price='1')
    smp_ui.add_service_rule(rule_name='南京-洗车机费率1', rule_type='预付费-下发费用', rule_desc='南京-洗车机费率1描述', min_price='2',
                            expected_price='10')
    smp_ui.add_service_rule('南京-存储柜费率1', '后付费-上报业务量', '南京-存储柜费率1描述',
                            fee_rate_list=[['100L', '小时', '2'], ['50L', '小时', '1'], ['10L', '小时', '0.5']])
    smp_ui.driver.get(SMP_URL_SERVICE)

    yield

    sleep(1)
    smp_ui.driver.get(SMP_URL_DEVICE_MODEL)
    while True:
        del_bool = smp_ui.del_newly_added_item()
        if not del_bool:
            break

    sleep(1)
    smp_ui.driver.get(SMP_URL_SERVICE_RULE)
    sleep(1)

    while True:
        del_bool = smp_ui.del_newly_added_item()
        if not del_bool:
            break


@pytest.fixture(scope='function')
def del_newly_added_service_rule():
    yield
    print('删除添加的设备')
    smp_ui.del_newly_added_item()


def test_smp_service_001(into_service_mgr, del_newly_added_service_rule):
    smp_ui.add_service('电瓶车充电站', 'bokpower-charger-g22-220v450w', '全国-电瓶车充电费率1')
    services = smp_ui.list_all_devices()
    assert services == [[
        '电瓶车充电站',
        'bokpower-charger-g22-220v450w',
        '电瓶车充电站_全国-电瓶车充电费率1',
        '全国-电瓶车充电费率1',
        '电瓶车充电站_全国-电瓶车充电费率1描述'
    ]]


def test_smp_service_101(into_service_mgr, del_newly_added_service_rule):
    smp_ui.add_service('洗车站', 'njcw-carwasher-g22-2s', '南京-洗车机费率1')
    services = smp_ui.list_all_devices()
    assert services == [[
        '洗车站',
        'njcw-carwasher-g22-2s',
        '洗车站_南京-洗车机费率1',
        '南京-洗车机费率1',
        '洗车站_南京-洗车机费率1描述'
    ]]


def test_smp_service_201(into_service_mgr, del_newly_added_service_rule):
    smp_ui.add_service('汽车充电站', 'yixun-charger-g22-220v7kw', '南京-存储柜费率1')
    services = smp_ui.list_all_devices()
    assert services == [[
        '汽车充电站',
        'yixun-charger-g22-220v7kw',
        '汽车充电站_南京-存储柜费率1',
        '南京-存储柜费率1',
        '汽车充电站_南京-存储柜费率1描述'
    ]]
