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
Location = r"CSV_Data/test.csv"

# Create dataframe out of CSV data
Headers = ['No', 'Time', 'Type', 'Order', 'Size',
           'Price', 'SL', 'TP', 'Profit', 'Balance']
df = pd.read_csv(Location, names=Headers,  encoding="ISO-8859-1")

# df.info(verbose=True)

# Remove unnecessary columns
del df["SL"]
del df["TP"]
del df["Balance"]
del df["Size"]

# Create arrays to hold extracted data
OrderNumberArray = []
OrderTypeArray = []
OpenTimeArray = []
CloseTimeArray = []
OpenPriceArray = []
ClosePriceArray = []
ProfitArray = []

# Extract data
for row in df.itertuples():
    if (row[0] % 2) == 0:
        OrderNumberArray.append(row[4])
        OrderTypeArray.append(row[3])
        OpenTimeArray.append(row[2])
        OpenPriceArray.append(row[5])
    if (row[0] % 2) != 0:
        CloseTimeArray.append(row[2])
        ClosePriceArray.append(row[5])
        ProfitArray.append(row[6])

data = {"OrderNumber": OrderNumberArray, "OrderType": OrderTypeArray, "OpenTime": OpenTimeArray,
        "CloseTime": CloseTimeArray, "OpenPrice": OpenPriceArray, "ClosePrice": ClosePriceArray, "Profit": ProfitArray}

columnNames = ["OrderNumber", "OrderType", "OpenTime",
               "CloseTime", "OpenPrice", "ClosePrice", "Profit"]

# Overwrite existing dataframe
df = pd.DataFrame(data, columns=columnNames)

todaysDate = date.today().strftime("%Y_%m_%d")
newCSVName = "ProcessedData/" + todaysDate + "_CleanedOrdersList"
df.to_csv(newCSVName, index=False)

# Convert OpenTime/CloseTime to datetime
df["OpenTime"] = pd.to_datetime(df["OpenTime"], format="%Y.%m.%d %H:%M")
df["CloseTime"] = pd.to_datetime(df["CloseTime"], format="%Y.%m.%d %H:%M")

# Extract Open/CloseTime and convert to DayOfWeek
OpenTimeDayArray = []
CloseTimeDayArray = []
for row in df.itertuples():
    OpenTimeDayArray.append(row[3].dayofweek)
    CloseTimeDayArray.append(row[4].dayofweek)

df.insert(3, "OrderOpenDay", OpenTimeDayArray)
df.insert(5, "OrderCloseDay", CloseTimeDayArray)

# print(df)

# Groupby date
groupedByDate = df.groupby(df["OpenTime"].dt.date)["Profit"].agg(
    [np.ma.count, np.sum, np.mean, np.median, stats.mode, np.ptp, stats.iqr, np.std, "min", "max"])

# Groupby week - This gives week as numbers in the year
groupedByWeek = df.groupby(df["OpenTime"].dt.week)["Profit"].agg(
    [np.ma.count, np.sum, np.mean, np.median, stats.mode, np.ptp, stats.iqr, np.std, "min", "max"])

# Groupby week - This gives weeks as dates
df_ByWeek = df.set_index("OpenTime")

df_ByWeek = df_ByWeek.to_period(freq="w")

df_ByWeek = df_ByWeek.reset_index()

groupedByWeek = df_ByWeek.groupby(df_ByWeek["OpenTime"])["Profit"].agg(
    [np.ma.count, np.sum, np.mean, np.median, stats.mode, np.ptp, stats.iqr, np.std, "min", "max"])


# Groupby Month

df_ByMonth = df.set_index("OpenTime")

df_ByMonth = df_ByMonth.to_period(freq="m")

df_ByMonth = df_ByMonth.reset_index()

groupedByMonth = df_ByMonth.groupby(df_ByMonth["OpenTime"])["Profit"].agg(
    [np.ma.count, np.sum, np.mean, np.median, stats.mode, np.ptp, stats.iqr, np.std, "min", "max"])

# Convert all to dataframes

df_GroupedByDate = DataFrame(groupedByDate).reset_index()
df_GroupedByWeek = DataFrame(groupedByWeek).reset_index()
df_GroupedByMonth = DataFrame(groupedByMonth).reset_index()

# Save dataframes to CSV

#

print(df_GroupedByWeek)
