import pytest
from lib.webui_smp import smp_ui
from time import sleep


@pytest.fixture(scope='package', autouse=True)
def into_system_mgr():
    smp_ui.login('byhy', 'sdfsdf')
    sleep(1)
    yield
    # 结束之后退出登录
    smp_ui.logout()
