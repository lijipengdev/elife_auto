from selenium.webdriver.common.by import By
from lib.webui_smp import smp_ui
import pytest
from time import sleep

pytestmark = [pytest.mark.网页测试, pytest.mark.登录测试]


def test_smp_correct_login_001():
    smp_ui.login('byhy', 'sdfsdf')
    sleep(1)
    nav_ele = smp_ui.driver.find_elements(By.TAG_NAME, 'nav')
    assert nav_ele != []


@pytest.fixture
def clear_alert():
    yield
    try:
        smp_ui.driver.switch_to.alert.accept()
    except Exception as e:
        print(e)


@pytest.mark.parametrize('username, password, expected_alert', [
    (None, 'sdfsdf', '请输入用户名'),
    ('byhy', None, '请输入密码'),
    ('byhy', 'sdfsdfs', '登录失败： 用户名或者密码错误'),
    ('byhy', 'sdfsd', '登录失败： 用户名或者密码错误'),
    ('byhyb', 'sdfsdf', '登录失败： 用户名不存在'),
    ('byh', 'sdfsdf', '登录失败： 用户名不存在')
]
                         )
def test_smp_wrong_login_002_007(username, password, expected_alert, clear_alert):
    alert_text = smp_ui.login(username, password)
    sleep(1)
    alert_text = smp_ui.driver.switch_to.alert.text
    assert alert_text == expected_alert



