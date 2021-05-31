import numpy
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt


def band_power(x, fs, fmin, fmax):
    f, Pxx = scipy.signal.periodogram(x, fs=fs)
    ind_min = numpy.argmax(f > fmin) - 1
    ind_max = numpy.argmax(f > fmax) - 1
    return numpy.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


if __name__ == '__main__':
    f = open("resources/files/IOC-L09 - MI_BCIdataset.dat", "r")

    no_channels = int(f.readline())
    no_samples = int(f.readline())
    no_trial = int(f.readline())
    f.readline()
    freq = int(f.readline())
    f.readline()
    f.readline()
    left_hand_values = np.array(f.readline().strip().split("  "))
    f.readline()
    f.readline()
    f.readline()

    channel_1_left = []
    channel_1_right = []
    channel_2_left = []
    channel_2_right = []

    for value in left_hand_values:
        ch1_val = np.array(f.readline().strip().split(" ")).astype(float, casting='unsafe')
        ch2_val = np.array(f.readline().strip().split(" ")).astype(float, casting='unsafe')
        f.readline()

        if value == "1":
            channel_1_left.append(ch1_val)
            channel_2_left.append(ch2_val)
        else:
            channel_1_right.append(ch1_val)
            channel_2_right.append(ch2_val)

    channel_1_left_pw = []
    channel_1_right_pw = []
    channel_2_left_pw = []
    channel_2_right_pw = []

    fs = 128
    fmin = 14
    fmax = 18

    for x in channel_1_left:
        channel_1_left_pw.append([])
        for i in range(0, len(x) - fs):
            channel_1_left_pw[-1].append(band_power(x[i:fs + i - 1], fs, fmin, fmax))

    for x in channel_1_right:
        channel_1_right_pw.append([])
        for i in range(0, len(x) - fs):
            channel_1_right_pw[-1].append(band_power(x[i:fs + i - 1], fs, fmin, fmax))

    for x in channel_2_left:
        channel_2_left_pw.append([])
        for i in range(0, len(x) - fs):
            channel_2_left_pw[-1].append(band_power(x[i:fs + i - 1], fs, fmin, fmax))

    for x in channel_2_right:
        channel_2_right_pw.append([])
        for i in range(0, len(x) - fs):
            channel_2_right_pw[-1].append(band_power(x[i:fs + i - 1], fs, fmin, fmax))

    channel_1_left_pw_avg = []
    channel_1_right_pw_avg = []
    channel_2_left_pw_avg = []
    channel_2_right_pw_avg = []

    for i in range(len(channel_1_left_pw[0])):
        avg = 0
        for x in channel_1_left_pw:
            avg = avg + x[i]
        channel_1_left_pw_avg.append(avg / len(channel_1_left_pw))

    for i in range(len(channel_1_right_pw[0])):
        avg = 0
        for x in channel_1_right_pw:
            avg = avg + x[i]
        channel_1_right_pw_avg.append(avg / len(channel_1_right_pw))

    for i in range(len(channel_2_left_pw[0])):
        avg = 0
        for x in channel_2_left_pw:
            avg = avg + x[i]
        channel_2_left_pw_avg.append(avg / len(channel_2_left_pw))

    for i in range(len(channel_2_right_pw[0])):
        avg = 0
        for x in channel_2_right_pw:
            avg = avg + x[i]
        channel_2_right_pw_avg.append(avg / len(channel_2_right_pw))

    x_target = []
    for i in range(len(channel_1_left_pw[0])):
        x_target.append(i / fs)

    plt.figure("graphics", figsize=(15, 15))
    red_x = [2, 2]
    red_y = [-20, 20]

    plt.subplot(331)
    plt.plot(x_target, channel_1_left_pw_avg, "g")
    plt.plot(x_target, channel_1_right_pw_avg, "b")
    plt.plot(red_x, red_y, "r")
    plt.ylim(0, 4)

    plt.subplot(332)
    plt.plot(x_target, channel_2_left_pw_avg, "g")
    plt.plot(x_target, channel_2_right_pw_avg, "b")
    plt.plot(red_x, red_y, "r")

    plt.ylim(0, 4)
    # plt.xlim(0, 0.7)
    # plt.xlabel('time [s]')
    # plt.ylabel('[uV]')
    # plt.grid()
    # plt.locator_params(axis="x", nbins=7)
    # plt.locator_params(axis="y", nbins=3)

    plt.legend(["Left", "Right"], bbox_to_anchor=(1.5, 0.5), loc='center', borderaxespad=0.)
    plt.show()
