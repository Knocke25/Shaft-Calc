# Python Project
# Brayden Knocke, Gharabet Torossian, Taylor Vazquez

from scipy.optimize import fsolve

from copy import deepcopy

import numpy as np

from matplotlib import pyplot as plt


class Shaft:
    # initialize variables
    def __init__(self, ):
        self.title = None
        self.dist_unit = None
        self.force_unit = None
        self.Sut = None
        self.Sy = None
        self.Se = None
        self.E = None

        self.fatigue_factor = None
        self.static_factor = None

        self.reliability = None
        self.temperature = None

        self.Stress_concentrations = None

        self.shaft_length = None

        self.loads = []                         # [[thrust, Fy, Fz, torque, My, Mz, Delta, Slope(rad), location, width]]
                                                #  0        1    2    3     4   5     6       7          8         9
        self.Thrust_bearings = []               # [Slope, location, width, min_ID
        self.Radial_bearing = []

        self.diameters = []
        self.diameter_vals = []

        self.diameter_count = None

        self.R_thrust_y = None
        self.R_radial_y = None
        self.R_thrust_z = None
        self.R_radial_z = None

        self.my_vals = None
        self.mz_vals = None
        self.m_vals = None

        self.maxMoment = None
        self.maxM_location = None

        self.thrust = None
        self.thrust_vals = []
        self.torque_vals = []

        self.maxTorque = None
        self.maxTorque_location = None

        self.diameter_x = []

        self.axial_stress = []
        self.torsional_stress = []
        self.bending_stress = []
        self.static_stress = []

        self.max_mean = None
        self.max_mean_location = None

        self.max_amplidue_stress = None
        self.max_amplidue_stress_location = None

        self.max_static_stress = None
        self.max_static_stress_location = None

        self.Fss = []

        self.min_fs_static = None
        self.min_fs_static_location = None

        self.Fsf = []

        self.min_fs_fatigue = None
        self.min_fs_fatigue_location = None
        self.maxThrust = None
        self.maxThrust_location = None

        self.mean_stress = []
        self.amplidue_stress = []

    def processShaftData(self, data): # needs to have (self, data)

            for line in data:  # loop over all the lines
                cells = line.strip().split(',')
                keyword = cells[0].lower()

                if keyword == 'title': self.title = cells[1].strip().replace("'", "")
                if keyword == 'distance_unit': self.dist_unit = cells[1].strip().replace("'", "")
                if keyword == 'force_unit': self.force_unit = cells[1].strip().replace("'", "")
                if keyword == 'fatigue_factor': self.fatigue_factor = float(cells[1])
                if keyword == 'static_factor': self.static_factor = float(cells[1])
                if keyword == 'shaft_length': self.shaft_length = float(cells[1])
                if keyword == 'reliability': self.reliability = float(cells[1])
                if keyword == 'temperature': self.temperature = float(cells[1])
                if keyword == 'stress_concentrations': self.Stress_concentrations = float(cells[1])

                if keyword == 'material':
                    self.Sut = float(cells[1])
                    self.Sy = float(cells[2])
                    self.Se = float(cells[3])
                    self.E = float(cells[4])

                if keyword == 'load':
                    thrust = float(cells[1])
                    Fy = float(cells[2])
                    Fz = float(cells[3])
                    torque = float(cells[4])
                    My = float(cells[5])
                    Mz = float(cells[6])
                    delta = float(cells[7])
                    slope = float(cells[8])
                    location = float(cells[9])
                    width = float(cells[10])
                    this_load = [thrust, Fy, Fz, torque, My, Mz, delta, slope, location, width]
                    self.loads.append(this_load)

                if keyword == 'thrust_bearing':
                    slope = float(cells[1])
                    location = float(cells[2])
                    width = float(cells[3])
                    min_ID = float(cells[4])
                    this_load = [slope, location, width, min_ID]
                    self.Thrust_bearings = this_load

                if keyword == 'radial_bearing':
                    slope = float(cells[1])
                    location = float(cells[2])
                    width = float(cells[3])
                    min_ID = float(cells[4])
                    this_load = [slope, location, width, min_ID]
                    self.Radial_bearing = this_load

                if keyword == 'diameters':
                    i = 1
                    self.diameter_count = (len(cells) - 1) / 2
                    while i < len(cells):
                        location = float(cells[i].replace("(", "").replace(")", ""))
                        diameter = float(cells[i+1].replace("(", "").replace(")", ""))
                        this_one = [location, diameter]
                        self.diameters.append(this_one)
                        i += 2

    def solve(self):
        qy = []
        for i in range(len(self.loads)):
            qy.append([self.loads[i][1], self.loads[i][8], -1])
            qy.append([self.loads[i][5], self.loads[i][8], -2])
            # singularity equation (without R1 and R2)

        qz = []
        for i in range(len(self.loads)):
            qz.append([self.loads[i][2], self.loads[i][8], -1])
            qz.append([self.loads[i][4], self.loads[i][8], -2])

        def diameters_values(eqn):
            xxxxx = np.linspace(self.shaft_length / 100000.0, self.shaft_length, 3000)
            i =1
            j = 0
            output = np.zeros(len(xxxxx))
            eqn.append([self.shaft_length, 0])
            for n in xxxxx:
                if n <= eqn[i][0]:
                    output[j] = eqn[i-1][1]
                else:
                    output[j] = eqn[i][1]
                    i+= 1
                j += 1
            return output

        def integrate(eqn):                                             # Integration function for singularity functions
            for n in range(0, len(eqn)):
                eqn[n][2] = eqn[n][2] + 1
                if eqn[n][2] > 1:
                    eqn[n][0] = eqn[n][0] / (eqn[n][2])
            return eqn

        def find_max_thrust(eqn):                                            # finds the max shear magnitude and location
            max = eqn[0][0]
            place = eqn[0][1]
            for n in range(0, len(eqn)):
                if abs(eqn[n][0]) > abs(max):
                    max = eqn[n][0]
                    place = eqn[n][1]
            ans = max, place
            return ans

        def find_max_torque(eqn):                                            # finds the max shear magnitude and location
            max = eqn[0][0]
            place = eqn[0][1]
            for n in range(0, len(eqn)):
                if abs(eqn[n][0]) > abs(max):
                    max = eqn[n][0]
                    place = eqn[n][1]
            ans = max, place
            return ans

        def find_max_Moment(eqn):                                       # finds max moment magnitude and location
            max = abs(eqn[0][0])
            place = eqn[0][1]
            for n in range(0, len(eqn)):
                if abs(eqn[n][0]) > max:
                    max = abs(eqn[n][0])
                    place = eqn[n][1]
            ans = max, place
            return ans

        def shear_eqn(eqn):                                             # shear equation for sum of forces in y-dir
            ans = 0
            for n in range(0, len(eqn)):
                if eqn[n][2] == -1:
                    ans = ans + eqn[n][0]
            return ans

        def moment_eqn(eqn):                                            # moment equation for sum of moments and point 0
            ans = 0

            for n in range(0, len(eqn)):
                if eqn[n][2] == -2:
                    ans = ans + eqn[n][0]
                elif eqn[n][2] == -1:
                    ans = ans + (-eqn[n][0] * eqn[n][1])
            return ans

        def equations_y(p):                                               # equation to then solve for reactions
            R_thrust, R_radial = p
            shear = shear_eqn(qy)
            moment = moment_eqn(qy)
            return (shear + R_thrust + R_radial, moment - R_thrust*self.Thrust_bearings[1] - R_radial*(self.Radial_bearing[1]))

        def equations_z(p):                                               # equation to then solve for reactions
            R_thrust, R_radial = p
            shear = shear_eqn(qz)
            moment = moment_eqn(qz)
            return (shear + R_thrust + R_radial, moment - R_thrust*self.Thrust_bearings[1] - R_radial*(self.Radial_bearing[1]))

        def SngEqnVals_shear(snglist, x, c1=0, c2=0):                   # shear values at each time slot
            # x is a list of values and snglist is list of singularity functions
            # get a x long list of values for each time slot
            ans = np.zeros(shape=(len(x), 2))
            i = 0
            for n in x:
                for m in range(0, len(snglist)):
                    if n >= snglist[m][1]:
                        if snglist[m][2] == 0:
                            ans[i][0] = ans[i][0] + snglist[m][0]

                ans[i][1] = n
                i += 1

            return ans

        def thrust_values(list, x):                   # shear values at each time slot
            # x is a list of values and snglist is list of singularity functions
            # get a x long list of values for each time slot
            ans = np.zeros(shape=(len(x), 2))
            i = 0
            for n in x:
                for m in range(0, len(list)):
                    if n >= list[m][8]:
                        ans[i][0] = ans[i][0] + list[m][0]

                ans[i][1] = n
                i += 1

            return ans

        def torque_values(list, x):                   # shear values at each time slot
            # x is a list of values and snglist is list of singularity functions
            # get a x long list of values for each time slot
            ans = np.zeros(shape=(len(x), 2))
            i = 0
            for n in x:
                for m in range(0, len(list)):
                    if n >= list[m][8]:
                        ans[i][0] = ans[i][0] + list[m][3]

                ans[i][1] = n
                i += 1

            return ans

        def SngEqnVals_moment(snglist, x, c1=0, c2=0):                 # moment values at each time slot
            # x is a list of values and snglist is list of singularity functions
            # get a x long list of values for each time slot
            ans = np.zeros(shape=(len(x), 2))

            i = 0
            for n in x:
                for m in range(0, len(snglist)):
                    if n >= snglist[m][1]:
                        if snglist[m][2] == 1:
                            temp = snglist[m][0] * (n - snglist[m][1] )
                            ans[i][0] = ans[i][0] + temp
                        elif snglist[m][2] == 0:
                            ans[i][0] = ans[i][0] + snglist[m][0]
                ans[i][1] = n
                i += 1

            return ans

        def SqrtOfSquares(list1, list2):
            output = np.zeros(shape=(len(list1), 2))
            for i in range(len(list1)):
                output[i][1] = list1[i][1]
                list1_squared = list1[i][0]**2
                list2_squared = list2[i][0]**2
                close = list2_squared+list1_squared
                output[i][0] = np.sqrt(close)
            return output

        def calc_thrust(list):
            output = 0
            for i in range(len(list)):
                output = output + list[i][0]
            return output

        def calc_axial_stress(torque_vals, diameters):
            axial_stress = np.zeros(len(diameters))
            for i in range(len(diameters)):
                area = (np.pi*diameters[i]**2)/4
                axial_stress[i] = torque_vals[i]/area
            return axial_stress

        def calc_torsional_stress(torque_vals, diameters):
            torsional_stress = np.zeros(len(diameters))
            for i in range(len(diameters)):
                j = (np.pi*diameters[i]**4)/32
                radius = diameters[i]/2
                torsional_stress[i] = (torque_vals[i]*radius)/j
            return torsional_stress

        def calc_bending_stress(moment, diameter):
            bending_stress = np.zeros(len(diameter))
            for n in range(len(diameter)):
                I = (np.pi*diameter[n]**4)/64
                radius = diameter[n]/2
                bending_stress[n] = (moment[n]*radius) / I
            return bending_stress

        def calc_mean_stress(axial, torsion):
            mean_stress = np.zeros(len(axial))
            for i in range(len(axial)):
                axial_squared = axial[i]**2
                torsional_squared = torsion[i]**2
                torsional_squared_3 = torsional_squared *3
                mean_stress[i] = np.sqrt(axial_squared + torsional_squared_3)
            return mean_stress

        def find_max_mean(L, eqn):                                            # finds the max shear magnitude and location
            xxxxx = np.linspace(L / 100000.0, L, 3000)
            max = eqn[0]
            place = xxxxx[0]
            for n in range(0, len(eqn)):
                if abs(eqn[n]) > abs(max):
                    max = eqn[n]
                    place = xxxxx[n]
            ans = max, place
            return ans

        def calc_amplitude_stress(Kf, bending):                                 # ignore Kf for this project
            output = np.zeros(len(bending))
            for i in range(len(bending)):
                output[i] = bending[i] * 1
            return output

        def find_max_amplitude(L, eqn):                                            # finds the max shear magnitude and location
            xxxxx = np.linspace(L / 100000.0, L, 3000)
            max = eqn[0]
            place = xxxxx[0]
            for n in range(0, len(eqn)):
                if abs(eqn[n]) > abs(max):
                    max = eqn[n]
                    place = xxxxx[n]
            ans = max, place
            return ans

        def calc_static_stress(axial, bending, torsional):
            output = np.zeros(len(axial))
            for i in range(len(bending)):
                axial_plus_bending = (abs(axial[i]) + bending[i])**2
                torsional_squared = (torsional[i]**2)*3
                output[i] = np.sqrt(axial_plus_bending+torsional_squared)
            return output

        def static_FS(Sy, static):
            output = np.zeros(len(static))
            Sy = Sy *1000
            for i in range(len(static)):
                output[i] =Sy/static[i]
            return output

        def find_min_Fs(L, eqn):                                            # finds the max shear magnitude and location
            xxxxx = np.linspace(L / 100000.0, L, 3000)
            min = eqn[0]
            place = xxxxx[0]
            for n in range(0, len(eqn)):
                if abs(eqn[n]) < abs(min):
                    min = eqn[n]
                    place = xxxxx[n]
            ans = min, place
            return ans

        def fatigue_FS(Se, Sut, amplitude, mean, Kf):
            output = np.zeros(len(amplitude))
            for i in range(len(amplitude)):
                amp_Se = amplitude[i] / (Se *1000)
                mean_Sut = mean[i] / (Sut * 1000)
                both = amp_Se + mean_Sut

                if both == 0:
                    output[i] = 99999999
                else:
                    almost = 1 / both
                    output[i] = almost
            return output

        def add_stress_concentrations(Kf, L, diameters, bending):
            i = 1
            for n in range(1, len(diameters)):
                this = diameters[n]
                that = diameters[n-1]
                if this != that:
                    if diameters[n-1] > diameters[n]:
                        bending[n] = bending[n] * Kf
                    else:
                        bending[n] = bending[n-1] * Kf
                else:
                    nothing = 0
                i += 1
            return bending
        # actual solving

        self.diameter_vals = diameters_values(self.diameters)

        # Solve for the reaction forces in y-dir for the supports
        self.R_thrust_y, self.R_radial_y = fsolve(equations_y, (250, 56))
        r_thrust_y = [[self.R_thrust_y, self.Thrust_bearings[1], -1]]
        r_radial_y = [[self.R_radial_y, self.Radial_bearing[1], -1]]

        # Solve for the reaction forces in z-dir for the supports
        self.R_thrust_z, self.R_radial_z = fsolve(equations_z, (250, 56))
        r_thrust_z = [[self.R_thrust_z, self.Thrust_bearings[1], -1]]
        r_radial_z = [[self.R_radial_z, self.Radial_bearing[1], -1]]
        # new singularity function with supports
        qy = qy + r_thrust_y + r_radial_y
        qz = qz + r_thrust_z + r_radial_z

        # integrate each function to get all equations needed
        qy_temp = deepcopy(qy)
        qz_temp = deepcopy(qz)
        Vy = integrate(deepcopy(qy_temp))
        Vz = integrate(deepcopy(qz_temp))
        My = integrate(integrate(deepcopy(qy_temp)))
        Mz = integrate(integrate(deepcopy(qz_temp)))

        # set some variables needed
        L = self.shaft_length
        xxxxx =np.linspace(L / 100000.0, L, 3000)

        # calculate moment values and max point
        sng_vals_My = SngEqnVals_moment(My, xxxxx)
        self.my_vals = sng_vals_My[:, 0]

        sng_vals_Mz = SngEqnVals_moment(Mz, xxxxx)
        self.mz_vals = sng_vals_Mz[:, 0]

        total_m = SqrtOfSquares(sng_vals_My, sng_vals_Mz)
        self.m_vals = total_m[:,0]

        self.maxMoment, self.maxM_location = find_max_Moment(total_m)

        self.thrust = abs(calc_thrust(self.loads))
        thrust_for_axial_graph = [[self.thrust, 0, 0, 0, 0, 0, 0, 0, self.Thrust_bearings[1], 0]]
        loads_with_thrust = self.loads + thrust_for_axial_graph
        thrust = thrust_values(loads_with_thrust, xxxxx)
        self.thrust_vals = thrust[:,0]
        self.maxThrust, self.maxThrust_location = find_max_thrust(thrust)

        torque = torque_values(self.loads, xxxxx)
        self.torque_vals = torque[:, 0]

        self.maxTorque, self.maxTorque_location = find_max_torque(torque)

        self.axial_stress = calc_axial_stress(self.thrust_vals, self.diameter_vals)
        self.torsional_stress = calc_torsional_stress(self.torque_vals, self.diameter_vals)
        self.bending_stress = calc_bending_stress(self.m_vals, self.diameter_vals)
        self.mean_stress = calc_mean_stress(self.axial_stress, self.torsional_stress)
        self.max_mean, self.max_mean_location = find_max_mean(self.shaft_length, self.mean_stress)
        self.amplidue_stress = calc_amplitude_stress(self.Stress_concentrations, self.bending_stress)
        self.max_amplidue_stress, self.max_amplidue_stress_location = find_max_amplitude(self.shaft_length, self.amplidue_stress)
        self.static_stress = calc_static_stress(self.axial_stress, self.bending_stress, self.torsional_stress)
        self.max_static_stress, self.max_static_stress_location = find_max_amplitude(self.shaft_length, self.static_stress)

        self.Fss = static_FS(self.Sy, self.static_stress)
        self.min_fs_static, self.min_fs_static_location = find_min_Fs(self.shaft_length, self.Fss)

        self.amplidue_stress = add_stress_concentrations(self.Stress_concentrations, self.shaft_length, self.diameter_vals, self.amplidue_stress)
        self.Fsf = fatigue_FS(self.Se, self.Sut, self.amplidue_stress, self.mean_stress, self.Stress_concentrations)
        self.min_fs_fatigue, self.min_fs_fatigue_location = find_min_Fs(self.shaft_length, self.Fsf)

    def plot_moments(self, L, my_vals, mz_vals, m_vals):

        xxxxx = np.linspace(L / 100000.0, L, 3000)

        plt.rcParams["figure.figsize"] = [16, 16]
        plt.rcParams.update({'font.size': 18})
        fig, axarr = plt.subplots(3, sharex=True)
        plt.suptitle('Moments', fontsize=36)
        fig.patch.set_facecolor('WhiteSmoke')

        axarr[0].plot(xxxxx, my_vals, linewidth=3)
        axarr[0].set_title('x-y plane')
        axarr[0].locator_params(axis='y', nbins=2)

        axarr[1].plot(xxxxx, mz_vals, linewidth=3)
        axarr[1].set_title('x-z plane')
        axarr[1].locator_params(axis='y', nbins=2)

        axarr[2].plot(xxxxx, m_vals, linewidth=3)
        axarr[2].set_title('vector magnitude')
        axarr[2].locator_params(axis='y', nbins=2)

        plt.show()

    def plot_axial(self, L, thrust_vals, torque_vals):
        xxxxx = np.linspace(L / 100000.0, L, 3000)

        plt.rcParams["figure.figsize"] = [16, 16]
        plt.rcParams.update({'font.size': 18})
        fig, axarr = plt.subplots(2, sharex=True)
        plt.suptitle('Axial-force and Torque Diagrams', fontsize=36)
        fig.patch.set_facecolor('WhiteSmoke')

        axarr[0].plot(xxxxx, thrust_vals, linewidth=3)
        axarr[0].set_title('Axial Force')
        axarr[0].locator_params(axis='y', nbins=2)

        axarr[1].plot(xxxxx, torque_vals, linewidth=3)
        axarr[1].set_title('Torque')
        axarr[1].locator_params(axis='y', nbins=2)


        plt.show()

    def plot_stresses(self, L, axial_stress, bending, statics):
        xxxxx = np.linspace(L / 100000.0, L, 3000)

        plt.rcParams["figure.figsize"] = [16, 16]
        plt.rcParams.update({'font.size': 18})
        fig, axarr = plt.subplots(3, sharex=True)
        plt.suptitle('Axial-force and Torque Diagrams', fontsize=36)
        fig.patch.set_facecolor('WhiteSmoke')

        axarr[0].plot(xxxxx, axial_stress, linewidth=3)
        axarr[0].set_title('Axial Force')
        axarr[0].locator_params(axis='y', nbins=2)

        axarr[1].plot(xxxxx, bending, linewidth=3)
        axarr[1].set_title('Bending Stress')
        axarr[1].locator_params(axis='y', nbins=2)

        axarr[2].plot(xxxxx, statics, linewidth=3)
        axarr[2].set_title('Static Stress')
        axarr[2].locator_params(axis='y', nbins=2)

        plt.show()

    def plot_diameters(self, L, diameters):
        xxxxx = np.linspace(L / 100000.0, L, 3000)
        plt.plot(xxxxx, diameters)
        plt.show()