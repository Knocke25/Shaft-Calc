# Python Project
# To be used with Shaft Design Input files
# Brayden Knocke, Gharabet Torossian, Taylor Vazquez
import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from Shaft_ui import Ui_Dialog
from Shaft_project import Shaft


class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.assign_widgets()
        self.Shaft = None
        self.show()

    def assign_widgets(self):
        self.ui.pushButton_Exit.clicked.connect(self.ExitApp)
        self.ui.pushButton_GetShaft.clicked.connect(self.GetShaft)
        self.ui.pushButton_PlotAxTor_3.clicked.connect(self.ClearDiameters)
        self.ui.pushButton_Moments.clicked.connect(self.plot_moments)
        self.ui.pushButton_PlotDiameters.clicked.connect(self.plot_diameters)
        self.ui.pushButton_PlotAxTor.clicked.connect(self.plot_axial)
        self.ui.pushButton_PlotStresses.clicked.connect(self.plot_stresses)

    def GetShaft(self):

        # get the filename using the OPEN dialog
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:
            no_file()
            return
        self.ui.textEdit_filename.setText(filename)
        app.processEvents()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # Read the file
        f1 = open(filename, 'r')  # open the file for reading
        data = f1.readlines()  # read the entire file as a list of strings
        f1.close()  # close the file  ... very important

        self.Shaft = Shaft()  # create a wing instance (object)

        try:
            self.Shaft.processShaftData(data)
            self.ClearDiameters()
            self.Shaft.solve()
            self.ui.lineEdit_RRy.setText('{:.2f}'.format(self.Shaft.R_radial_y))
            self.ui.lineEdit_TRy.setText('{:.2f}'.format(self.Shaft.R_thrust_y))
            self.ui.lineEdit_RRz.setText('{:.2f}'.format(self.Shaft.R_radial_z))
            self.ui.lineEdit_TRz.setText('{:.2f}'.format(self.Shaft.R_thrust_z))
            self.ui.lineEdit_maxMoment.setText('{:.2f}'.format(self.Shaft.maxMoment))
            self.ui.lineEdit_maxMoment_loc.setText('{:.2f}'.format(self.Shaft.maxM_location))
            self.ui.lineEdit_Thrust.setText('{:.2f}'.format(self.Shaft.thrust))
            self.ui.lineEdit_maxTension.setText('{:.2f}'.format(self.Shaft.maxThrust))
            self.ui.lineEdit_maxTension_loc.setText('{:.2f}'.format(self.Shaft.maxThrust_location))
            self.ui.lineEdit_maxTorque.setText('{:.2f}'.format(self.Shaft.maxTorque))
            self.ui.lineEdit_maxTorque_loc.setText('{:.2f}'.format(self.Shaft.maxTorque_location))
            self.ui.lineEdit_maxSigm.setText('{:.2f}'.format(self.Shaft.max_mean))
            self.ui.lineEdit_maxSigm_loc.setText('{:.2f}'.format(self.Shaft.max_mean_location))
            self.ui.lineEdit_maxSiga.setText('{:.2f}'.format(self.Shaft.max_amplidue_stress))
            self.ui.lineEdit_maxSiga_loc.setText('{:.2f}'.format(self.Shaft.max_amplidue_stress_location))
            self.ui.lineEdit_maxStatic.setText('{:.2f}'.format(self.Shaft.max_static_stress))
            self.ui.lineEdit_maxStatic_loc.setText('{:.2f}'.format(self.Shaft.max_static_stress_location))
            self.ui.lineEdit_minFSstatic.setText('{:.2f}'.format(self.Shaft.min_fs_static))
            self.ui.lineEdit_minFSstatic_loc.setText('{:.2f}'.format(self.Shaft.min_fs_static_location))
            self.ui.lineEdit_FS_Static_Reqd.setText('{:.2f}'.format(self.Shaft.static_factor))
            self.ui.lineEdit_FS_Fatigue_Reqd.setText('{:.2f}'.format(self.Shaft.fatigue_factor))
            self.ui.lineEdit_minFSfatigue.setText('{:.2f}'.format(self.Shaft.min_fs_fatigue))
            self.ui.lineEdit_minFSfatigue_loc.setText('{:.2f}'.format(self.Shaft.min_fs_fatigue_location))
            # self.ui.lineEdit_maxSigm.setText('{:.2f}'.format(self.Shaft.maxTorque))
            # self.ui.lineEdit_maxSigm_loc.setText('{:.2f}'.format(self.Shaft.maxTorque_location))
            # self.ui.lineEdit_d1.setText('{:.7f}'.format(self.Shaft.diameters[1]))
            # self.ui.lineEdit_d2_loc.setText('{:.7f}'.format(self.Shaft.diameters[2]))
            # self.ui.lineEdit_d2.setText('{:.7f}'.format(self.Shaft.diameters[3]))

            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()
            bad_file()

    def Diameters(self):
        i = 0
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d1_loc.setText('{:.2f}'.format(self.Shaft.diameters[0][0]))
            self.ui.lineEdit_d1.setText('{:.2f}'.format(self.Shaft.diameters[0][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d2_loc.setText('{:.2f}'.format(self.Shaft.diameters[1][0]))
            self.ui.lineEdit_d2.setText('{:.2f}'.format(self.Shaft.diameters[1][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d3_loc.setText('{:.2f}'.format(self.Shaft.diameters[2][0]))
            self.ui.lineEdit_d3.setText('{:.2f}'.format(self.Shaft.diameters[2][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d4_loc.setText('{:.2f}'.format(self.Shaft.diameters[3][0]))
            self.ui.lineEdit_d4.setText('{:.2f}'.format(self.Shaft.diameters[3][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d5_loc.setText('{:.2f}'.format(self.Shaft.diameters[4][0]))
            self.ui.lineEdit_d5.setText('{:.2f}'.format(self.Shaft.diameters[4][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d6_loc.setText('{:.2f}'.format(self.Shaft.diameters[5][0]))
            self.ui.lineEdit_d6.setText('{:.2f}'.format(self.Shaft.diameters[5][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d7_loc.setText('{:.2f}'.format(self.Shaft.diameters[6][0]))
            self.ui.lineEdit_d7.setText('{:.2f}'.format(self.Shaft.diameters[6][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d8_loc.setText('{:.2f}'.format(self.Shaft.diameters[7][0]))
            self.ui.lineEdit_d8.setText('{:.2f}'.format(self.Shaft.diameters[7][1]))
        i += 1
        if self.Shaft.diameter_count > i:
            self.ui.lineEdit_d9_loc.setText('{:.2f}'.format(self.Shaft.diameters[8][0]))
            self.ui.lineEdit_d9.setText('{:.2f}'.format(self.Shaft.diameters[8][1]))

    def ClearDiameters(self):
        self.ui.lineEdit_d1_loc.setText('')
        self.ui.lineEdit_d1.setText('')
        self.ui.lineEdit_d2_loc.setText('')
        self.ui.lineEdit_d2.setText('')
        self.ui.lineEdit_d3_loc.setText('')
        self.ui.lineEdit_d3.setText('')
        self.ui.lineEdit_d4_loc.setText('')
        self.ui.lineEdit_d4.setText('')
        self.ui.lineEdit_d5_loc.setText('')
        self.ui.lineEdit_d5.setText('')
        self.ui.lineEdit_d6_loc.setText('')
        self.ui.lineEdit_d6.setText('')
        self.ui.lineEdit_d7_loc.setText('')
        self.ui.lineEdit_d7.setText('')
        self.ui.lineEdit_d8_loc.setText('')
        self.ui.lineEdit_d8.setText('')
        self.ui.lineEdit_d9_loc.setText('')
        self.ui.lineEdit_d9.setText('')
        self.Diameters()

    def PlotSomething(self):

        self.beam.plot(title=self.beam.title)

    def plot_moments(self):
        self.Shaft.plot_moments(self.Shaft.shaft_length,
                                self.Shaft.my_vals, self.Shaft.mz_vals,
                                self.Shaft.m_vals)

    def plot_diameters(self):
        self.Shaft.plot_diameters(self.Shaft.shaft_length, self.Shaft.diameter_vals)

    def plot_axial(self):
        self.Shaft.plot_axial(self.Shaft.shaft_length, self.Shaft.thrust_vals, self.Shaft.torque_vals)

    def plot_stresses(self):
        self.Shaft.plot_stresses(self.Shaft.shaft_length, self.Shaft.mean_stress, self.Shaft.bending_stress, self.Shaft.static_stress)

    def ExitApp(self):
        app.exit()


def no_file():
    msg = QMessageBox()
    msg.setText('There was no file selected')
    msg.setWindowTitle("No File")
    retval = msg.exec_()
    return None


def bad_file():
    msg = QMessageBox()
    msg.setText('Unable to process the selected file')
    msg.setWindowTitle("Bad File")
    retval = msg.exec_()
    return None


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())