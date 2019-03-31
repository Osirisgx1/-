    # -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 10:44:18 2019

@author: lxy
"""
import os
#******** UI ***********
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from my_AQI_ui_final import Ui_MainWindow
import sys,time
#********数据接口***********
import json
import requests    
#获取数据函数
def process(url):
    r = requests.get(url)
    hjson = json.loads(r.text)
    if (isinstance(hjson,list)==False):
        return 0
    else:
        return hjson
#图形界面设置
class mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        #按钮连接
        self.pushButton.clicked.connect(self.get_AQI_data)
        #插入一个LCD时间显示
        self.lcdNumber.display(time.strftime("%X",time.localtime()))
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.setMode(QLCDNumber.Dec)
        #新建一个QTimer对象
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        # 信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)
    #使LCD显示当前时间
    def onTimerOut(self):
        self.lcdNumber.display(time.strftime("%X",time.localtime()))
    #获取AQI数据
    def get_AQI_data(self):
        #输入城市
        city_name = self.lineEdit.text()
        #设置初始内容
        content = ''
        #获取API数据
        url = 'http://www.pm25.in/api/querys/co.json?city='+str(city_name)+'&token=5j1znBVAsnSf5xQyNQyq'
        my_data = process(url)
        AQI_dict = my_data
        #筛选有效数据保存到本地
        if ( my_data != 0 ):
            
            with open( "F:\\PB16020656 刘潇扬\\data\\" + str(my_data[-1]['area'])+'data.json', "w") as f:
                js = json.dumps(my_data, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
                f.write(js)
        if  (AQI_dict  ==  0):
            #无数据报错
            self.textEdit.setText("你输入的城市名有误，或者未收录你所在城市")
        else:
            #在文本框1输出该城市总体数据
            self.textEdit.setText(
                '城市：'+AQI_dict[-1].get('area')+'\n'
                '空气质量：'+str(AQI_dict[-1].get('quality'))+'\n'
                'AQI：'+ str(AQI_dict[-1].get('aqi'))+'\n'          
                'CO：'+str(AQI_dict[-1].get('co'))+'\n'
                '主要污染物：'+str(AQI_dict[-1].get('primary_pollutant'))+'\n'
                '日期：'+str(AQI_dict[-1].get('time_point'))
                )
            
            for i,items in enumerate(AQI_dict):
                #筛选有效监测站数据
                area = AQI_dict[i].get('position_name')
                #增加监测站内容
                if (isinstance(area,str)==True):
                    content = content + (
                    '监测站：'+str(area)+'\n'
                    '空气质量：'+ str(AQI_dict[i].get('quality')) +'\n'
                    'AQI：'+ str(AQI_dict[i].get('aqi'))+'\n'
                    'CO：'+str(AQI_dict[i].get('co'))+'\n'
                    '主要污染物：'+str(AQI_dict[i].get('primary_pollutant'))+'\n'
                    
                    '**********************\n'
                    )
                #在文本框2输出该城市观测站数据
                self.textEdit_2.setText(content)
                

if __name__ == "__main__":
    app = 0
    app = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(app.exec())
