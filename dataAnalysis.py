import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import grangercausalitytests
import cpi

# Read in targets
targets_df = pd.read_csv('targets.csv')
targets_df['Date'] = pd.to_datetime(targets_df['Date'])
targets_df.set_index('Date', inplace=True)

# Read in predictors
predictors_df = pd.read_csv('predictors.csv')
predictors_df['Date'] = pd.to_datetime(predictors_df['Date'])
predictors_df.set_index('Date', inplace=True)

# Merge targets and predictors
merged_data = targets_df.join(predictors_df)
print(merged_data)








