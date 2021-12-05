  
"""
@Author: Mohammad Fatha
@Date: 2021-11-24
@Last Modified by: Mohammad Fatha
@Title : Real Time Stock Data plot 
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas 
import pyarrow.parquet as pq
import numpy as np

def animate(i):
    data = pq.read_table('/home/fatha/Desktop/Prediction/RealTimeStockDataPrediction.parquet/part-00000-07763280-dd5e-4575-803e-32feb2497eb9-c000.snappy.parquet').to_pandas()
    df = data.iloc[:100]
    x1 = df['time']
    y1 = df['close']
    y2 = df['prediction']
    plt.cla()
    plt.scatter(x1,y1,label="Actual Values", color='r')
    plt.plot(x1,y2,label="Predicted Values", color='y')
    plt.xlabel("Time")
    plt.ylabel("Stock data values")
    plt.legend()
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()