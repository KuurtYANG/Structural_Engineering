"""
function "eccs" applies the ECCS method to calculate the yield load
"""
import numpy as np
import pandas as pd
import scipy as sp
import scipy.optimize
import os
import matplotlib.pyplot as plt

class Yield():
    def __init__(self, df_data, per_y0):
        self.df_data = df_data
        self.per_y0 = per_y0

    def eccs(self):
        x = np.array(self.df_data.iloc[1:,0], dtype=float) # start from 0
        x = x[~np.isnan(x)] # remove the missing data
        y = np.array(self.df_data.iloc[1:,1], dtype=float)
        max_y = max(y)
        max_x = x[np.argmax(y)]

        for i0, y0 in enumerate(y):
            if y0 > self.per_y0*max_y: # find the end point of elastic range according to self.per_y0
                break    
        def linear(x, k1):
            return k1*x  
        pro, _ = sp.optimize.curve_fit(linear, x[:i0+1], y[:i0+1]) # include x[i]
        pro = pro[0]
        
        for k in range(1000):     
            k1, b1 = pro/10, max_y*(1000-k)/1000 
            for j1, x1 in enumerate(x[i0+1:]):
                y1 = y[i0+1+j1]
                if y1 > k1*x1+b1:
                    sta_c = 1 # intersection happens
                    break
                else:
                    sta_c = 0                 
            if sta_c == 1:
                break
            else:
                continue # lower the crossing line gradually
                
        xc = b1/(pro-k1) # x- and y-values of the point of intersection
        yc = pro*b1/(pro-k1)

        plt.figure(figsize=[10, 6])
        ax = plt.axes()
        ax.plot(x, y, '-', linewidth=2) 
        x = np.arange(0,xc*1.3)
        y = pro*x
        ax.plot(x, y, '-g')
        x = np.arange(0,max_x)
        y = k1*x + b1
        ax.plot(x, y, '-r')
        ax.annotate("(%s,%s)" % (round(xc,2),round(yc,2)), xy=(xc,yc), xytext=(-70, 10), textcoords='offset points')
        ax.grid(True, linestyle='-.')
        ax.set(xlabel='Displacement (mm)', ylabel='Force (N)')
        plt.show()

print(os.getcwd())
df = pd.read_excel("./Structural_Engineering/Yield_load/Force_Displacement.xls")
yield_calc = Yield(df, 0.6)
yield_calc.eccs()