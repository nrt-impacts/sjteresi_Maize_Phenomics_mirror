from matplotlib import pyplot


def hist_height(arr, imgname):
    pyplot.hist(arr)
    pyplot.xlabel("Height (ft above sea level)")
    pyplot.ylabel("Frequency")
    pyplot.savefig(imgname)
    pyplot.clf()
