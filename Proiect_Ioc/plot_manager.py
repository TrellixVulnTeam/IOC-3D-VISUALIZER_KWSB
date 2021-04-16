import numpy
import numpy as np
import matplotlib.pyplot as plt


class PlotManager:
    def __init__(self):
        self.target, self.freq_target, self.no_samples_target = self.read_data("resources/files/ep8chTargets.dat")
        self.non_target, self.freq_non_target, self.no_samples_non_target = self.read_data(
            "resources/files/ep8chNONTargets.dat")

    def read_data(self, path):
        f = open(path, "r")

        no_channels = int(f.readline())
        no_samples = int(f.readline())
        no_trial = int(f.readline())
        f.readline()
        freq = int(f.readline())

        data = []

        for t in range(no_trial):
            data.append([])
            for c in range(no_channels):
                x = np.array(f.readline().strip().split(" "))
                data[t].append(x.astype(float, casting='unsafe'))
            f.readline()
        return data, freq, no_samples

    def apply_correction(self, data):
        limit = 26

        for t in range(len(data)):
            for c in range(len(data[t])):
                avg = 0
                for i in range(limit):
                    avg = avg + data[t][c][i]
                avg = avg / limit
                for i in range(len(data[t][c])):
                    data[t][c][i] = data[t][c][i] - avg

    def plot_data(self):
        self.apply_correction(self.target)
        self.apply_correction(self.non_target)

        target_plot = []

        for c in range(len(self.target[0])):
            avg_values = self.target[0][c]
            for t in range(1, len(self.target)):
                avg_values = avg_values + self.target[t][c]
            avg_values = avg_values / len(self.target)
            target_plot.append(avg_values)

        non_target_plot = []

        for c in range(len(self.non_target[0])):
            avg_values = self.non_target[0][c]
            for t in range(1, len(self.non_target)):
                avg_values = avg_values + self.non_target[t][c]
            avg_values = avg_values / len(self.non_target)
            non_target_plot.append(avg_values)

        x_target = []
        x_non_target = []

        for i in range(self.no_samples_target):
            x_target.append(i / self.freq_target)

        for i in range(self.no_samples_non_target):
            x_non_target.append(i / self.freq_non_target)

        plt.figure("graphics", figsize=(15, 15))
        maxim = max(target_plot[0])

        for i in range(len(target_plot)):
            maxim = max(maxim, max(max(target_plot[i]), max(non_target_plot[i])))

        red_x = [0.1, 0.1]
        red_y = [-20, 20]

        for i in range(len(target_plot)):
            plt.subplot(330 + i + 1)
            plt.plot(x_target, target_plot[i], "y")
            plt.plot(x_non_target, non_target_plot[i], "b")
            plt.plot(red_x, red_y, "r")
            plt.ylim(-maxim - 1, maxim + 1)
            plt.xlim(0, 0.7)
            plt.xlabel('time [s]')
            plt.ylabel('[uV]')
            plt.grid()
            plt.locator_params(axis="x", nbins=7)
            plt.locator_params(axis="y", nbins=3)

        plt.legend(["Target", "NONtarget", "Trigger"], bbox_to_anchor=(1.5, 0.5), loc='center', borderaxespad=0.)
        plt.show()
