from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
from cfg import *
from selenium.webdriver.support.ui import Select


class SMP_UI:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 本地无需驱动，为了避免浏览器升级后驱动不匹配，该行代码会去网上自动下载当前浏览器版本对应的驱动
        os.environ['SE_DRIVER_MIRROR_URL'] = 'https://cdn.npmmirror.com/binaries/chrome-for-testing'
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login(self, username, password):
        self.driver.get(SMP_URL_LOGIN)
        sleep(1)
        if username is not None:
            self.driver.find_element(By.ID, 'username').send_keys(username)
        if password is not None:
            self.driver.find_element(By.ID, 'password').send_keys(password)
        sleep(1)
        self.driver.find_element(By.ID, 'loginBtn').click()
        sleep(1)

    def logout(self):
        sleep(1)
        # 点击1号超级管理员
        self.driver.find_element(By.ID, 'top-right').click()
        sleep(1)
        # 点击退出
        self.driver.find_element(By.XPATH, '//li[text()="退出"]').click()
        sleep(1)

    '''
    设备类型
    '''

    def add_device_model(self, device_type, device_model, device_model_desc):
        sleep(1)
        # 点击添加按钮
        top_btn = smp_ui.driver.find_element(By.CSS_SELECTOR, '.add-one-area > span')
        if top_btn.text == '添加':
            top_btn.click()
            sleep(1)
        # 输入设备种类，设备型号，型号描述
        # 创建Select对象
        select = Select(self.driver.find_element(By.ID, 'device-type'))
        # 通过Select对象选中存储柜
        select.select_by_visible_text(device_type)
        # 设备型号输入
        device_type_ele = self.driver.find_element(By.ID, 'device-model')
        device_type_ele.send_keys(device_model)
        # 型号描述输入
        device_model_ele = self.driver.find_element(By.ID, 'device-model-desc')
        device_model_ele.send_keys(device_model_desc)
        # 点击确定
        self.driver.find_element(By.CSS_SELECTOR, '.add-one-submit-btn-div .btn').click()
        # 睡一秒保证数据可以正常显示在列表上
        sleep(1)

        # 添加数据后清除历史输入避免影响下次测试,这里的设备种类无法取消选中，采用刷新页面后，重新点击添加
        self.driver.refresh()
        # 点击添加按钮
        top_btn = smp_ui.driver.find_element(By.CSS_SELECTOR, '.add-one-area > span')
        if top_btn.text == '添加':
            top_btn.click()
            sleep(1)

    def list_all_device_models(self):
        sleep(1)
        # 第一个等待时间是0，
        self.driver.implicitly_wait(0)
        values = self.driver.find_elements(By.CSS_SELECTOR, '.field-value')
        # 如果能找到下一页的话就点击下一页
        next_page_ele = self.driver.find_elements(By.XPATH, '//span[text()="下一页"][not(contains(@class,"disable"))]')
        while True:
            next_page_ele = self.driver.find_elements(By.XPATH, '//span[text()="下一页"][not(contains(@class,"disable"))]')
            if next_page_ele:
                next_page_ele[0].click()
                sleep(1)
                values += self.driver.find_elements(By.CSS_SELECTOR, '.field-value')
            else:
                break
        print(values)
        device_models = []
        for index, value in enumerate(values):
            if (index + 1) % 3 == 0:
                device_models.append([values[index - 2].text, values[index - 1].text, values[index].text])

        return device_models

    # 该函数的返回值是一个布尔类型，返回是否删除成功
    def del_newly_added_item(self) -> bool:
        sleep(1)
        self.driver.implicitly_wait(0)
        del_btn = self.driver.find_elements(By.CSS_SELECTOR,
                                            '.result-list-item:first-child .result-list-item-btn-bar .btn-no-border:first-child')
        self.driver.implicitly_wait(10)
        if not del_btn:
            return False

        del_btn[0].click()
        self.driver.switch_to.alert.accept()
        return True

    # 修改设备类型
    def update_device_model(self, device_model, device_model_desc) -> bool:
        sleep(1)
        self.driver.implicitly_wait(0)
        update_btn = self.driver.find_elements(By.CSS_SELECTOR,
                                               '.result-list-item:first-child .result-list-item-btn-bar .btn-no-border:last-child')
        self.driver.implicitly_wait(10)
        if not update_btn:
            return False
        update_btn[0].click()
        sleep(1)
        device_model_ele = self.driver.find_element(By.XPATH,
                                                    '//div[@class="edit-one-form"]//span[text()="设备型号"]/following-sibling::*')
        device_model_ele.clear()
        device_model_ele.send_keys(device_model)
        device_model_desc_ele = self.driver.find_element(By.XPATH,
                                                         '//div[@class="edit-one-form"]//span[text()="型号描述"]/following-sibling::*')
        device_model_desc_ele.clear()
        device_model_desc_ele.send_keys(device_model_desc)

        # 点击确定
        self.driver.find_element(By.CSS_SELECTOR, '.result-list-item-btn-bar .btn-no-border:first-child').click()
        sleep(1)

    '''
    业务规则
    '''

    def add_service_rule(self, rule_name: str, rule_type: str, rule_desc: str, min_price=None,
                         expected_price=None,
                         service_code=None,
                         charge_unit=None, unit_price=None, fee_rate_list=None
                         ):
        sleep(1)
        # 点击添加按钮
        top_btn = smp_ui.driver.find_element(By.CSS_SELECTOR, '.add-one-area > span')
        if top_btn.text == '添加':
            top_btn.click()
            sleep(1)
        # 输入规则名称
        rule_name_ele = self.driver.find_element(By.XPATH,
                                                 '//div[@class="add-one-area"]//span[text()="规则名称"]/following-sibling::*')
        rule_name_ele.clear()
        rule_name_ele.send_keys(rule_name)
        # 输入规则类型
        # 创建Select对象
        select = Select(self.driver.find_element(By.ID, 'rule_type_id'))
        # 通过Select对象选中存储柜
        select.select_by_visible_text(rule_type)
        sleep(1)
        # 输入最小消费
        self.driver.implicitly_wait(0)
        min_price_ele = self.driver.find_elements(By.XPATH,
                                                  '//div[@class="add-one-area"]//span[text()="最小消费"]/following-sibling::*')
        self.driver.implicitly_wait(10)
        if min_price_ele:
            min_price_ele[0].clear()
            min_price_ele[0].send_keys(min_price)
        sleep(1)
        # 输入预估消费
        self.driver.implicitly_wait(0)
        expected_price_ele = self.driver.find_elements(By.XPATH,
                                                       '//div[@class="add-one-area"]//span[text()="预估消费"]/following-sibling::*')
        self.driver.implicitly_wait(10)
        if expected_price_ele:
            expected_price_ele[0].clear()
            expected_price_ele[0].send_keys(expected_price)
        sleep(1)
        # 输入计费单位
        self.driver.implicitly_wait(0)
        charge_unit_ele = self.driver.find_elements(By.XPATH,
                                                    '//div[@class="add-one-area"]//span[text()="计费单位"]/following-sibling::*[1]')
        self.driver.implicitly_wait(10)
        if charge_unit_ele and rule_type != '后付费-上报业务量':
            charge_unit_ele[0].clear()
            charge_unit_ele[0].send_keys(charge_unit)
        # 输入单位价格
        sleep(1)
        self.driver.implicitly_wait(0)
        unit_price_ele = self.driver.find_elements(By.XPATH,
                                                   '//div[@class="add-one-area"]//span[text()="单位价格"]/following-sibling::*[1]')
        self.driver.implicitly_wait(10)
        if unit_price_ele and rule_type != '后付费-上报业务量':
            unit_price_ele[0].clear()
            unit_price_ele[0].send_keys(unit_price)
        sleep(1)
        # 循环输入费率
        if rule_type == '后付费-上报业务量':
            for index, fee_rate in enumerate(fee_rate_list, 1):
                service_code = fee_rate[0]
                charge_unit = fee_rate[1]
                unit_price = fee_rate[2]
                self.driver.implicitly_wait(0)
                service_code_ele = self.driver.find_elements(By.XPATH,
                                                             f'//div[@class="fee-rate-list"]/div[@class="fee-rate"][{index}]/span[text()="业务码"]/following-sibling::*[1]')
                self.driver.implicitly_wait(10)
                if service_code_ele:
                    service_code_ele[0].clear()
                    service_code_ele[0].send_keys(service_code)

                sleep(1)
                self.driver.implicitly_wait(0)
                charge_unit_ele = self.driver.find_elements(By.XPATH,
                                                            f'//div[@class="fee-rate-list"]/div[@class="fee-rate"][{index}]/span[text()="计费单位"]/following-sibling::*[1]')
                self.driver.implicitly_wait(10)
                if charge_unit_ele:
                    charge_unit_ele[0].clear()
                    charge_unit_ele[0].send_keys(charge_unit)
                sleep(1)
                self.driver.implicitly_wait(0)
                unit_price_ele = self.driver.find_elements(By.XPATH,
                                                           f'//div[@class="fee-rate-list"]/div[@class="fee-rate"][{index}]/span[text()="单位价格"]/following-sibling::*[1]')
                self.driver.implicitly_wait(10)
                if unit_price_ele:
                    unit_price_ele[0].clear()
                    unit_price_ele[0].send_keys(unit_price)
                sleep(1)
                # 首次添加结束后，点击添加费率，如果达到列表的最大长度，就不点击添加按钮了
                if index != len(fee_rate_list):
                    self.driver.find_element(By.XPATH, '//button[text()="添加费率"]').click()
        # 输入规则描述
        self.driver.find_element(By.XPATH,
                                 '//div[@class="add-one-area"]//span[text()="规则描述"]/following-sibling::*').send_keys(
            rule_desc)
        # 点击确定
        self.driver.find_element(By.CSS_SELECTOR, '.add-one-submit-btn-div .btn').click()
        # 睡一秒保证数据可以正常显示在列表上
        sleep(1)

        # 添加数据后清除历史输入避免影响下次测试,这里的设备种类无法取消选中，采用刷新页面后，重新点击添加
        self.driver.refresh()
        # 点击添加按钮
        top_btn = smp_ui.driver.find_element(By.CSS_SELECTOR, '.add-one-area > span')
        if top_btn.text == '添加':
            top_btn.click()
            sleep(1)

    def list_all_rules(self, rule_type):
        sleep(1)
        # 第一个等待时间是0，
        self.driver.implicitly_wait(0)
        values = self.driver.find_elements(By.CSS_SELECTOR, '.field-value,.sub-field-value')
        # 如果能找到下一页的话就点击下一页
        if rule_type != '后付费-上报业务量':
            while True:
                next_page_ele = self.driver.find_elements(By.XPATH,
                                                          '//span[text()="下一页"][not(contains(@class,"disable"))]')
                if next_page_ele:
                    next_page_ele[0].click()
                    sleep(1)
                else:
                    break
        print(values)
        service_rules = []
        if rule_type == '预付费-下发业务量':
            for index, value in enumerate(values):
                if (index + 1) % 8 == 0:
                    service_rules.append(
                        [values[index - 7].text, values[index - 6].text, values[index - 4].text, values[index - 3].text,
                         values[index - 2].text.split('：')[1].strip(), values[index - 1].text.split('：')[1].strip(),
                         values[index].text])
            print(service_rules)
        elif rule_type == '预付费-下发费用':
            for index, value in enumerate(values):
                if (index + 1) % 6 == 0:
                    service_rules.append(
                        [values[index - 5].text, values[index - 4].text, values[index - 2].text, values[index - 1].text,
                         values[index].text])
            print(service_rules)
        else:
            items = self.driver.find_elements(By.CSS_SELECTOR, '.result-list-item')
            for index, item in enumerate(items):
                values = item.find_elements(By.CSS_SELECTOR, '.field-value,.sub-field-value')
                for idx, value in enumerate(values):
                    print(len(values))
                    if (idx + 1) % len(values) == 0:
                        rule_content_length = len(values) - 4
                        rule_content_list = []
                        count = int(rule_content_length / 3)
                        for j in range(count):
                            rule_content_list.append(
                                [values[idx - (len(values) - 3 * (j + 1)) + 1].text.split('：')[1].strip(),
                                 values[idx - (len(values) - 3 * (j + 1) - 1) + 1].text.split('：')[1].strip(),
                                 values[idx - (len(values) - 3 * (j + 1) - 2) + 1].text.split('：')[1].strip()])
                        service_rules.append(
                            [values[idx - (len(values) - 1)].text, values[idx - (len(values) - 2)].text,
                             rule_content_list,
                             values[idx].text])
            while True:
                next_page_ele = self.driver.find_elements(By.XPATH,
                                                          '//span[text()="下一页"][not(contains(@class,"disable"))]')
                if next_page_ele:
                    next_page_ele[0].click()
                    sleep(1)
                    items = self.driver.find_elements(By.CSS_SELECTOR, '.result-list-item')
                    for index, item in enumerate(items):
                        values = item.find_elements(By.CSS_SELECTOR, '.field-value,.sub-field-value')
                        for idx, value in enumerate(values):
                            print(len(values))
                            if (idx + 1) % len(values) == 0:
                                rule_content_length = len(values) - 4
                                rule_content_list = []
                                count = int(rule_content_length / 3)
                                for j in range(count):
                                    rule_content_list.append(
                                        [values[idx - (len(values) - 3 * (j + 1)) + 1].text.split('：')[1].strip(),
                                         values[idx - (len(values) - 3 * (j + 1) - 1) + 1].text.split('：')[1].strip(),
                                         values[idx - (len(values) - 3 * (j + 1) - 2) + 1].text.split('：')[
                                             1].strip()])
                                service_rules.append(
                                    [values[idx - (len(values) - 1)].text, values[idx - (len(values) - 2)].text,
                                     rule_content_list,
                                     values[idx].text])
                else:
                    break
        print(service_rules)

        return service_rules

    '''
    设备管理
    '''

    def add_service(self, device_type, device_model, service_rule):
        sleep(1)
        # 点击添加按钮
        top_btn = smp_ui.driver.find_element(By.CSS_SELECTOR, '.add-one-area > span')
        if top_btn.text == '添加':
            top_btn.click()
            sleep(1)
        # 创建Select对象
        select = Select(self.driver.find_element(By.ID, 'device-type'))
        # 通过Select对象选中设备类型
        select.select_by_visible_text(device_type)
        # 选择设备型号
        select = Select(self.driver.find_element(By.ID, 'device-model'))
        # 通过Select对象选中设备类型
        select.select_by_visible_text(device_model)
        # 创建Select对象
        select = Select(self.driver.find_element(By.ID, 'svc-rule-id'))
        # 通过Select对象选中业务规则
        select.select_by_visible_text(service_rule)
        # 输入设备编号
        self.driver.find_element(By.ID, 'device-sn').send_keys(device_type + '_' + service_rule)
        # 输入设备描述
        self.driver.find_element(By.ID, 'device-desc').send_keys(device_type + '_' + service_rule + '描述')
        # 点击确定
        self.driver.find_element(By.CSS_SELECTOR, '.add-one-submit-btn-div .btn').click()

        # 睡一秒保证数据可以正常显示在列表上
        sleep(1)

        # 添加数据后清除历史输入避免影响下次测试,这里的设备种类无法取消选中，采用刷新页面后，重新点击添加
        self.driver.refresh()
        # 点击添加按钮
        top_btn = smp_ui.driver.find_element(By.CSS_SELECTOR, '.add-one-area > span')
        if top_btn.text == '添加':
            top_btn.click()
            sleep(1)

    def list_all_devices(self):
        sleep(1)
        # 第一个等待时间是0，
        self.driver.implicitly_wait(0)
        values = self.driver.find_elements(By.CSS_SELECTOR, '.field-value')
        # 如果能找到下一页的话就点击下一页
        while True:
            next_page_ele = self.driver.find_elements(By.XPATH, '//span[text()="下一页"][not(contains(@class,"disable"))]')
            if next_page_ele:
                next_page_ele[0].click()
                sleep(1)
                values += self.driver.find_elements(By.CSS_SELECTOR, '.field-value')
            else:
                break
        print(values)
        device = []
        for index, value in enumerate(values):
            if (index + 1) % len(values) == 0:
                device.append([values[index - (len(values) - 1)].text, values[index - (len(values) - 2)].text,
                               values[index - (len(values) - 3)].text, values[index - (len(values) - 5)].text,
                               values[index].text])
        print(device)

        return device


smp_ui = SMP_UI()
