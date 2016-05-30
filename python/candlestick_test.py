import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

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
X_COORD_OFFSET_BUY_SETUP = 0.004
Y_COORD_OFFSET_BUY_SETUP = 0.1
Y_COORD_OFFSET_ANNOT = 0.2

def movingAvg(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas

def graphData(candle_data, MA1, MA2):
    try:
        # moving averages
        #av1 = movingAvg(closep, MA1)
        #av2 = movingAvg(closep, MA2)
        # starting_point = len(date[MA2-1:])

        ax1 = plt.subplot(1,1,1)
        ax1.set_axis_bgcolor(BG_GREY)
        candlestick_ohlc(ax1,candle_data, width=0.01, colorup=UP_GREEN,colordown=DOWN_RED)

        #ax1.plot(date[-starting_point:], av1[-starting_point:])
        #ax1.plot(date[-starting_point:], av2[-starting_point:])

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

        return ax1

    except Exception,e:
        print 'failed in graphData main loop', str(e)


def TD_Buy_Setup(candle_data, ax1):
    o = openp[::-1]
    h = highp[::-1]
    l = lowp[::-1]
    c = closep[::-1]
    end = len(candle_data) - 1

    for t in xrange(4,end):
        #print "> t" + str(t) + " o:" + str(o[t]) + " h:" + str(h[t]) + " l:" + str(l[t]) + " c:" + str(c[t])

        # TD Price Flip
        if c[t] > c[t-4] and c[t+1] < c[t-3]:
            ax1.annotate('^', (date[start_date - t-1] - X_COORD_OFFSET_BUY_SETUP, lowp[start_date - t-1] - Y_COORD_OFFSET_ANNOT), color=YELLOW)

            # TD Setup (in the next 9 time steps including price flip bar)
            TD_buy_setup_counter = 0
            for bear_t in xrange(t + 1, t + 10):
                #print "\t> bear t " + str(bear_t) + " o:" + str(o[bear_t]) + " h:" + str(h[bear_t]) + " l:" + str(l[bear_t]) + " c:" + str(c[bear_t])

                if c[bear_t] < c[bear_t - 4]:
                    TD_buy_setup_counter += 1

                    ax1.annotate(TD_buy_setup_counter, (date[start_date - bear_t] - X_COORD_OFFSET_BUY_SETUP , lowp[start_date - bear_t] - Y_COORD_OFFSET_BUY_SETUP), color=UP_GREEN)
                    if TD_buy_setup_counter >= 9:
                        #print "TD buy setup"

                        # Perfected ( low from 8 onwards < (low_6 and low_7) )
                        low_6 = l[bear_t - 3]
                        low_7 = l[bear_t - 2]

                        for perfected_t in xrange(bear_t - 1, end):
                            if l[perfected_t] < low_6 and l[perfected_t] < low_7:
                                #print "perfected"
                                ax1.annotate("^", (date[start_date - perfected_t] - X_COORD_OFFSET_BUY_SETUP , lowp[start_date - perfected_t] - Y_COORD_OFFSET_ANNOT), color=DOWN_RED)

                                # reset setup counter and exit the TD setup loop
                                TD_buy_setup_counter = 0
                                break

                else:
                    print "TD buy setup break"
                    TD_buy_setup_counter = 0
                    break


series = 'RXM6'

# load series data
series_file = DATA_FOLDER + series + '/' + series + '.csv'
date, openp, highp, lowp, closep = np.loadtxt(series_file,
                                              delimiter=',',
                                              unpack=True,
                                              converters={ 0: mdates.strpdate2num('%m/%d/%Y %H:%M:%S')})
# generate candlestick data
candle_data = []
for i in xrange(len(date)):
    appendLine = date[i], openp[i], highp[i], lowp[i], closep[i]
    candle_data.append(appendLine)

# x coord for annotate goes backwards, start from last value and count backward
start_date = len(date)-1

fig = plt.figure(facecolor=BG_GREY)
ax = graphData(candle_data,12,26)
TD_Buy_Setup(candle_data, ax)
plt.show()
fig.savefig(GRAPH_FOLDER+series+'.png', facecolor=fig.get_facecolor())