import pytest
from lib.webui_smp import smp_ui


# 测试结束后退出浏览器
@pytest.fixture(scope='session', autouse=True)
def quit_browser():
    yield
    smp_ui.driver.quit()
