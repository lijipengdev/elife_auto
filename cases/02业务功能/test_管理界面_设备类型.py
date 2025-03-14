from selenium.webdriver.common.by import By
from lib.webui_smp import smp_ui
import pytest
from time import sleep
from cfg import *

pytestmark = [pytest.mark.网页测试, pytest.mark.设备类型]


@pytest.fixture(scope='module')
def into_device_model_mgr():
    smp_ui.driver.get(SMP_URL_DEVICE_MODEL)
    sleep(1)
    yield


@pytest.fixture(scope='function')
def del_newly_added_device_model():
    yield
    print('删除添加的设备')
    smp_ui.del_newly_added_item()


@pytest.fixture(scope='function')
def an_electric_scooter_station():
    smp_ui.add_device_model('电瓶车充电站', 'bokpower-charger-g22-220v450w', '杭州bok 2022款450瓦 电瓶车充电站')
    yield
    smp_ui.del_newly_added_item()


def test_smp_device_model_001(into_device_model_mgr, del_newly_added_device_model):
    smp_ui.add_device_model('存储柜', 'elife-canbinlocker-g22-10-20-40', '南京e生活存储柜-10大20中40小')
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        "存储柜",
        'elife-canbinlocker-g22-10-20-40',
        '南京e生活存储柜-10大20中40小'
    ]]


def test_smp_device_model_002(into_device_model_mgr, del_newly_added_device_model):
    smp_ui.add_device_model('存储柜', 'a' * 100, '南京e生活存储柜-10大20中40小')
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '存储柜',
        'a' * 100,
        '南京e生活存储柜-10大20中40小'
    ]]


def test_smp_device_model_101(into_device_model_mgr, del_newly_added_device_model):
    smp_ui.add_device_model('电瓶车充电站', 'bokpower-charger-g22-220v450w', '杭州bok 2022款450瓦 电瓶车充电站')
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '电瓶车充电站',
        'bokpower-charger-g22-220v450w',
        '杭州bok 2022款450瓦 电瓶车充电站'
    ]]


def test_smp_device_model_201(into_device_model_mgr, del_newly_added_device_model):
    smp_ui.add_device_model('洗车站', 'njcw-carwasher-g22-2s', '南京e生活2022款洗车机 2个洗车位')
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '洗车站',
        'njcw-carwasher-g22-2s',
        '南京e生活2022款洗车机 2个洗车位'
    ]]


def test_smp_device_model_301(into_device_model_mgr, del_newly_added_device_model):
    smp_ui.add_device_model('汽车充电站', 'yixun-charger-g22-220v7kw', '南京易迅能源2022款7千瓦汽车充电站')
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '汽车充电站',
        'yixun-charger-g22-220v7kw',
        '南京易迅能源2022款7千瓦汽车充电站'
    ]]


def test_smp_device_model_501(into_device_model_mgr, an_electric_scooter_station):
    # 先列出系统中存在的一个电瓶车充电站，确认系统中是存在一个电瓶车充电站
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '电瓶车充电站',
        'bokpower-charger-g22-220v450w',
        '杭州bok 2022款450瓦 电瓶车充电站'
    ]]
    # 修改设备型号和型号描述后点击确定
    smp_ui.update_device_model('xiugaihoubokpower-charger-g22-220v450w', '修改后杭州bok 2022款450瓦 电瓶车充电站')
    # 再次列出系统中存在的设备
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '电瓶车充电站',
        'xiugaihoubokpower-charger-g22-220v450w',
        '修改后杭州bok 2022款450瓦 电瓶车充电站'
    ]]


def test_smp_device_model_601(into_device_model_mgr, an_electric_scooter_station):
    # 先列出系统中存在的一个电瓶车充电站，确认系统中是存在一个电瓶车充电站
    device_models = smp_ui.list_all_device_models()
    assert device_models == [[
        '电瓶车充电站',
        'bokpower-charger-g22-220v450w',
        '杭州bok 2022款450瓦 电瓶车充电站'
    ]]
    # 删除新创建的条目
    smp_ui.del_newly_added_item()
    # 再次列出系统中存在的设备
    device_models = smp_ui.list_all_device_models()
    assert device_models == []
