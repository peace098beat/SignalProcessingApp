from matplotlib import pyplot as plt


class LineBuilder:

    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):

        if event.inaxes is not self.line.axes:
            return

        print 'Click!!::', event

        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()



if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Click to build line segments')
    line, = ax.plot([0],[0])
    linebuilder = LineBuilder(line)

    plt.show()
