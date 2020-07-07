import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys  # Only needed to determine Python version
import matplotlib  # Only needed to determine Matplotlib version number
import chardet
from datetime import date
from pandas import DataFrame
from scipy import stats
import seaborn as sns

print('Python Version: ' + sys.version)
print('Pandas Version: ' + pd.__version__)
print('Matplotlib Version: ' + matplotlib.__version__)

# Import the csv data
Location = r"/Users/Pho/Documents/Freelance/Projects/GrahamStockTradingPlatform/Code/TradingScripts/StatsByDates/CSV_Data/test.csv"

# Create dataframe out of CSV data
Headers = ['No', 'Time', 'Type', 'Order', 'Size',
           'Price', 'SL', 'TP', 'Profit', 'Balance']
df = pd.read_csv(Location, names=Headers,  encoding="ISO-8859-1")
print(df)
