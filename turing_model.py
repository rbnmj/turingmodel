import numpy as np
import os

class TuringModel:
    def __init__(self, var, t, k_1, k_2, d_Hmax1, d_Hmax2):
        self.S = 4.8  # Nutrient supply concentration
        self.D = 0.3  # Dilution rate
        self.N_h = 1.5  # half saturation constant for nutrient uptake
        self.r_max = 0.7  # growth rate of autotroph
        self.h = 0.53  # handling time
        self.e = 0.33  # conversion efficiency of competitor
        self.d_N = 1  # Dispersal rate of nutrients
        self.d_A = 0.001  # dispersal rate of autotrophs
        self.a_1 = 1  # attack rate of competitor 1
        self.a_2 = 1  # attack rate of competitor 2
        self.k_1 = k_1  # dispersal adaptability for competitor 1
        self.k_2 = k_2  # dispersal adaptability for competitor 2
        self.d_Hmax1 = d_Hmax1  # maximum dispersal rate of competitor 1
        self.d_Hmax2 = d_Hmax2  # maximum dispersal rate of competitor 2
        self.t = t
        self.var = var
        self._equations(var, t)

    def _equations(self, var, t):
        # self.var = var
        # self.t = t
        # set parameters
        N_a = var[0]
        N_b = var[1]
        A_a = var[2]
        A_b = var[3]
        H_1a = var[4]
        H_1b = var[5]
        H_2a = var[6]
        H_2b = var[7]
        d_H1a = var[8]
        d_H2a = var[9]
        d_H1b = var[10]
        d_H2b = var[11]
        g_1a = var[12]
        g_1b = var[13]
        g_2a = var[14]
        g_2b = var[15]
        
        # growth rate of autotrophs
        r_a = (self.r_max * N_a) / (self.N_h + N_a)
        r_b = (self.r_max * N_b) / (self.N_h + N_b)

        # growth rate of competitors
        g_1a = (self.a_1 * A_a) / (1 + self.a_1 * self.h * A_a)
        g_1b = (self.a_1 * A_b) / (1 + self.a_1 * self.h * A_b)
        g_2a = (self.a_2 * A_a) / (1 + self.a_2 * self.h * A_a)
        g_2b = (self.a_2 * A_b) / (1 + self.a_2 * self.h * A_b)
        
        # inflection points
        x_01 = self.D / (self.a_1 * (self.e - self.h * self.D))
        x_02 = self.D / (self.a_2 * (self.e - self.h * self.D))

        # dispersal rates of competitors
        d_H1a = self.d_Hmax1 / (1 + np.exp(self.k_1 * (A_a - x_01)))
        d_H1b = self.d_Hmax1 / (1 + np.exp(self.k_1 * (A_b - x_01)))
        d_H2a = self.d_Hmax2 / (1 + np.exp(self.k_2 * (A_a - x_02)))
        d_H2b = self.d_Hmax2 / (1 + np.exp(self.k_2 * (A_b - x_02)))

        # change of nutrients
        dN_a = self.D * (self.S - N_a) - r_a * A_a + self.d_N * (N_b - N_a)
        dN_b = self.D * (self.S - N_b) - r_b * A_b + self.d_N * (N_a - N_b)

        # change of autotrophs
        dA_a = r_a * A_a - ((g_1a * H_1a) + (g_2a * H_2a)) - \
            self.D * A_a + self.d_A * (A_b - A_a)
        dA_b = r_b * A_b - ((g_1b * H_1b) + (g_2b * H_2b)) - \
            self.D * A_b + self.d_A * (A_a - A_b)

        # change of competitors
        dH_1a = self.e * g_1a * H_1a - self.D * H_1a - d_H1a * H_1a + d_H1b * H_1b
        dH_1b = self.e * g_1b * H_1b - self.D * H_1b - d_H1b * H_1b + d_H1a * H_1a
        dH_2a = self.e * g_2a * H_2a - self.D * H_2a - d_H2a * H_2a + d_H2b * H_2b
        dH_2b = self.e * g_2b * H_2b - self.D * H_2b - d_H2b * H_2b + d_H2a * H_2a

        H1_loss = d_H1a - (d_H1a * dH_1a) / \
            (1 + np.exp(self.k_1 * (A_a - x_01)))
        H2_loss = d_H2a - (d_H2a * dH_2a) / \
            (1 + np.exp(self.k_2 * (A_a - x_02)))
        
        #return (dN_a, dN_b, dA_a, dA_b, dH_1a, dH_1b, dH_2a, dH_2b, d_H1a, d_H2a, d_H1b, d_H2b, g_2a, g_2b)
        return (dN_a, dN_b, dA_a, dA_b, dH_1a, dH_1b, dH_2a, dH_2b, d_H1a, d_H2a, d_H1b, d_H2b, g_1a, g_1b, g_2a, g_2b)

    def equations_wrapper(var, t, model):
        return model._equations(var, t)

    def savedata(foldername, variable_library):
        data_folder = os.path.join(".", "data", foldername)
        os.makedirs(data_folder, exist_ok=True)

        for var_name, var_data in variable_library.items():
            np.savetxt(os.path.join(
                data_folder, f"{var_name}.csv"), var_data, delimiter=",")

        print("Data saved to ./data/" + foldername)

    def loaddata(foldername, variable_names):
        data_folder = os.path.join(".", "data", foldername)
        loaded_data = {}

        for var_name in variable_names:
            file_path = os.path.join(data_folder, f"{var_name}.csv")
            loaded_data[var_name] = np.loadtxt(file_path, delimiter=",")

        return loaded_data
