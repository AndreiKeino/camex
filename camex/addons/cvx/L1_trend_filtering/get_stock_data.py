#  https://stackoverflow.com/questions/55615969/python-how-to-get-stock-data-for-free-for-many-tickers-like-sp-500
# get the stock data and write in file
#  import pandas as pd
from pandas_datareader import data as wb
import os
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

ticker = 'BTC-USD'  # Bitcoin

num_save = 180
# num_save = 200

ticker = wb.DataReader(ticker, start='2015-1-1', data_source='yahoo')
close = ticker['Close'].to_numpy()
close = close[-num_save:]
print(close)
filename = (os.path.dirname(__file__) + os.path.sep
            + 'data' + os.path.sep + 'input_data.csv')
            # + 'data' + os.path.sep + 'bc.csv')
print('filename = ', filename)
np.savetxt(filename, close)

close_read = np.loadtxt(filename)

# close_read[0] += 0.0001

assert(np.array_equal(close, close_read))

plt.figure()
plt.plot(np.arange(len(close)), close)
plt.show()
