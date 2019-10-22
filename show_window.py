from 火车票助手 import get_stations,window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,datetime,time
"""显示信息提示框"""
def messgeDialog(title,message):
    msg_box = QMessageBox(QMessageBox.Warning,title,message)
    msg_box.exec_()
#主窗体的初始化类
class Main(QMainWindow,window.Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.model = QStandardItemModel()
        #根据控件自动改变列宽并且不可能修改宽度
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #设置表头不可见
        self.tableView.horizontalHeader().setVisible(False)
        #设置表格内容文字大小
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        #设置表格内容不可编辑
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #设置滚动条始终开启
        self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #查询按钮单击事件
    """查询按钮点击事件"""
    def on_click(self):
        # 获取数据
        get_from = self.textEdit.toPlainText()
        get_to = self.textEdit_2.toPlainText()
        get_date = self.textEdit_3.toPlainText()
        print(get_from)
        print(get_to)
        print(get_date)
        if get_stations.is_starts("staions.txt") == True:
            stations = eval(get_stations.read("staions.txt"))
            if get_from != "" and get_to != "" and get_date != "":
                # 判断输入的车站名称是否存在并正确
                if get_from in stations and get_to in stations and self.is_valid_date(get_date):
                    # 计算时间差
                    time_difference = self.time_difference(self.get_time(), get_date).days
                    # 判断时间差为0时证明是查询当前的车票,以及29天以后的车票
                    if time_difference >= 0 and time_difference <= 29:
                        from_station = stations[get_from]
                        to_station = stations[get_to]
                        # data = f"{get_date},{from_station},{to_station}"
                        data = get_stations.query(get_date, from_station, to_station)
                        print(data)
                        self.checkbox_default()
                        if len(data) != 0:
                            self.displayTable(len(data), 16, data)
                        else:
                            messgeDialog("警告", "没有返回网络数据")
                    else:
                        messgeDialog("警告", "超出查询日期的范围")
                else:
                    messgeDialog("警告", "车站的名称不存在或日期格式不正确")
            else:
                messgeDialog("警告", "请填写车站名称和日期")
        else:
            messgeDialog("警告", "去下载车站查询文件")
    """判断是否是正确的日期格式"""
    def is_valid_date(selfs,str):
        try:
            time.strptime(str,"%Y-%m-%d")
        except:
            return False
        else:
            return True
    """
    放入数据
    """
    def displayTable(self,train,info,data):
        self.model.clear()
        for row in range(train):
            for clounm in range(info):
                item = QStandardItem(data[row][clounm])
                self.model.setItem(row,clounm,item)
        print(self.model)
        self.tableView.setModel(self.model)
    """计算时间差方法"""
    def time_difference(self,in_time,new_time):
        in_time = time.strptime(in_time,"%Y-%m-%d")
        new_time = time.strptime(new_time,"%Y-%m-%d")
        #将struct时间对象转换为datetime对象
        in_time = datetime.datetime(in_time[0],in_time[1],in_time[2])
        new_time = datetime.datetime(new_time[0],new_time[1],new_time[2])
        #返回两个变量相差的值
        return new_time - in_time
    def get_time(self):
        # 获取当前时间戳
        now = int(time.time())
        # 转换为其他日期格式
        timeStruct = time.localtime(now)
        strTime = time.strftime("%Y-%m-%d", timeStruct)
        return strTime
    def checkbox_default(self):
        self.checkBox_G.setChecked(False)
        self.checkBox_D.setChecked(False)
        self.checkBox_K.setChecked(False)
        self.checkBox_T.setChecked(False)
        self.checkBox_Z.setChecked(False)
    #高铁复选框事件处理
    def change_G(self,state):
        #选中高铁信息添加到最后显示的数据当中
        if state == QtCore.Qt.Checked:
            #获取高铁信息
            get_stations.g_vehicle()
            #通过表格显示车型数据
            self.displayTable(len(get_stations.type_data),16,get_stations.type_data)
        else:
            #取消选中状态将移出数据
            get_stations.r_g_vehicle()
            if len(get_stations.type_data) == 0:
                self.displayTable(len(get_stations.data), 16, get_stations.data)
            else:
                self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
    #快速复选框
    def change_K(self, state):
        # 选中高铁信息添加到最后显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取高铁信息
            get_stations.k_vehicle()
            # 通过表格显示车型数据
            self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
        else:
            # 取消选中状态将移出数据
            get_stations.r_k_vehicle()
            if len(get_stations.type_data) == 0:
                self.displayTable(len(get_stations.data), 16, get_stations.data)
            else:
                self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
    # 特快速复选框
    def change_T(self, state):
        # 选中高铁信息添加到最后显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取高铁信息
            get_stations.t_vehicle()
            # 通过表格显示车型数据
            self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
        else:
            # 取消选中状态将移出数据
            get_stations.r_t_vehicle()
            if len(get_stations.type_data) == 0:
                self.displayTable(len(get_stations.data), 16, get_stations.data)
            else:
                self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
    # 动车复选框
    def change_D(self, state):
        # 选中高铁信息添加到最后显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取高铁信息
            get_stations.d_vehicle()
            # 通过表格显示车型数据
            self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
        else:
            # 取消选中状态将移出数据
            get_stations.r_d_vehicle()
            if len(get_stations.type_data) == 0:
                self.displayTable(len(get_stations.data), 16, get_stations.data)
            else:
                self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
    # 直达复选框
    def change_Z(self, state):
        # 选中高铁信息添加到最后显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取高铁信息
            get_stations.z_vehicle()
            # 通过表格显示车型数据
            self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
        else:
            # 取消选中状态将移出数据
            get_stations.r_z_vehicle()
            if len(get_stations.type_data) == 0:
                self.displayTable(len(get_stations.data), 16, get_stations.data)
            else:
                self.displayTable(len(get_stations.type_data), 16, get_stations.type_data)
"""启动窗体"""
def show_MainWindow():
    app = QApplication(sys.argv)
    main = Main()
    main.textEdit_3.setText(main.get_time())
    main.pushButton.clicked.connect(main.on_click)#查询按钮指定的单击事件
    #加入复选框功能
    main.checkBox_G.stateChanged.connect(main.change_G)
    main.checkBox_D.stateChanged.connect(main.change_D)
    main.checkBox_Z.stateChanged.connect(main.change_Z)
    main.checkBox_T.stateChanged.connect(main.change_T)
    main.checkBox_K.stateChanged.connect(main.change_K)
    main.show()#显示主窗体
    sys.exit(app.exec_())#循环中等待的时候退出循环
if __name__ == '__main__':
    # get_stations.get_station()
    # get_stations.Time()
    if get_stations.is_starts("staions.txt") == True and get_stations.is_starts("time.txt") == True:
        show_MainWindow()
    else:
        messgeDialog("警告","车站文件或起售实际文件出现异常")
