import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import _candlestick
import matplotlib
matplotlib.rcParams.update({'font.size': 9})

DATA_FOLDER = '../data/'
GRAPH_FOLDER = '../graphs/'
UP_GREEN = '#9eff15'
DOWN_RED = '#ff1717'
BG_GREY = '#585868'
WHITE = 'w'
YELLOW = '#FFF68F'
BLUE = '#5998ff'

def movingAvg(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas

def graphData(series,MA1,MA2):
    print 'loading',series
    try:
        # load series data
        series_file = DATA_FOLDER + series + '/' + series + '.csv'
        date, openp, highp, lowp, closep = np.loadtxt(series_file,
                                                      delimiter=',',
                                                      unpack=True,
                                                      converters={ 0: mdates.strpdate2num('%m/%d/%Y %H:%M:%S')})
        # generate candlestick data
        candle_data = []
        for i in xrange(len(date)):
            appendLine = date[i], openp[i], closep[i], highp[i], lowp[i]
            candle_data.append(appendLine)

        # moving averages
        av1 = movingAvg(closep, MA1)
        av2 = movingAvg(closep, MA2)

        starting_point = len(date[MA2-1:])


        # candlestick plot
        fig = plt.figure(facecolor=BG_GREY)
        ax1 = plt.subplot(1,1,1)
        ax1.set_axis_bgcolor(BG_GREY)
        _candlestick(ax1,candle_data, width=0.01, colorup=UP_GREEN,colordown=DOWN_RED)

        ax1.plot(date[-starting_point:], av1[-starting_point:])
        ax1.plot(date[-starting_point:], av2[-starting_point:])

        ax1.yaxis.label.set_color(YELLOW)
        ax1.xaxis.label.set_color(YELLOW)
        ax1.grid(True, color=YELLOW)
        ax1.spines['bottom'].set_color(BLUE)
        ax1.spines['top'].set_color(BLUE)
        ax1.spines['left'].set_color(BLUE)
        ax1.spines['right'].set_color(BLUE)
        ax1.tick_params(axis='y', colors=YELLOW)
        ax1.tick_params(axis='x', colors=YELLOW)
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y %H:%M:%S'))

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, hspace=.07)

        plt.ylabel('Price')
        plt.suptitle(series+' Price',color=YELLOW)
        plt.show()

        fig.savefig(GRAPH_FOLDER+series+'.png', facecolor=fig.get_facecolor())

    except Exception,e:
        print 'failed in graphData main loop', str(e)



series = 'RXM6'
graphData(series,12,26)
