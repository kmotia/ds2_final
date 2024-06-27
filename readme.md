# SO2 Emissions Nowcasting

This repository contains the code for my final project in Data Science II at the University of Vermont. The purpose of this project is to build a proof-of-concept pipeline for exploring exogenous industrial data to nowcast SO2 emissions data in the event of emission sensor failure.

## Project Overview

In this project, I compare various time-series methods for predicting SO2 emissions data:
- **SARIMAX** (Seasonal AutoRegressive Integrated Moving Average with eXogenous factors)
- **SARIMA** (Seasonal AutoRegressive Integrated Moving Average)
- Baseline time-series methods

## Methodology

1. **Data Collection**: Gathered industrial data relevant to SO2 emissions.
2. **Preprocessing**: Cleaned and prepared the data for analysis.
3. **Modeling**: Built and trained SARIMAX, SARIMA, and baseline models.
4. **Evaluation**: Compared the performance of each model in terms of accuracy and robustness.

## Usage
1. dataDownloader.py (data downloaded by this file is already housed in the repo)
   - Purpose: Downloads raw txt files for each pollutant.
   - Instructions:
     - Specify pollutant on line 40 in the script.
     - Files are stored in the "links" folder.
     - Requires signup username and password for NASA GES DISC (input in constants.py).
2. dataManipulator.py
3. dataCleaner.py
4. dataAnalysis.ipynb

### Instructions to Run Each File

1. dataDownloader.py
   - Downloads raw txt files for a specified pollutant.

2. dataManipulator.py
   - The script that manipulated pollutant emissions data observed multiple TXT files, each of which pertained a month of data from 1980 to 2023. Multiple pollutants were obtained in order to validate that their relative emissions agreed with general domain knowledge, which states that SO2 is a criteria air pollutant. Our script summed over the values in the file, and appended it to a list. The date for which each sum pertained was obtained by extracting information from the TXT file name. The resulting data was placed into a pandas dataframe and exported as a CSV file to be read in by the subsequent script for cleaning.

3. dataCleaner.py
   - Reads in the NASA and FRED data as CSV files, cleans them such that their time-series frequencies matched, and ensures variable units can rely on certain standards for easy interpretability. The technical parts of this process included downsampling the pollutant emissions data to a quarterly frequency. The data for each pollutant was then plotted to confirm that SO2 flux density emissions were higher relative to organic carbon emissions, black carbon emissions and SO4 emissions. Additionally, our process included adjusting financial data for inflation to use the value of the US dollar in 2023, and adjusting production index to use a base-year of 2023 for the value of 100 for all production volume data. The resulting data was exported to CSV files. Finally, the cleaned data was subject to the exploratory data analysis cycle during their analysis and modeling.

4. dataAnalysis.ipynb
   - The notebook used for analysis begins by merging the SO2 data with the data for the exogenous variables. Next, STL decomposition was performed in order to plot the observed, seasonal, and residual components of the data.
The purpose of this was to visually observe if the data was stationary, and if the residuals were independently and identically distributed (IDD). This important step served to make sure that the data satisfied the assumptions made by the SARIMAX and SARIMA models. We also observed the plots to identify any relationships between the exogenous variables and the SO2. We observed that the seasonality between the exogenous variables and SO2 were offset, indicating that a relationship between them might be lagged.
We performed an augmented Dicky-Fuller test to validate that the data was indeed non-stationary, and we explored differencing periods over which the data might become stationary. After exhausting differencing periods from 1 to 100, we decided to detrend the data to establish stationarity and potentially make the residuals IDD. However, we first split the SO2 and exogenous variables into their training and testing sets to prevent data leakage. After detrending the data, we checked if it was stationary using the augmented Dicky-Fuller test again, however, we did not check that the data had become IDD through testing. This could be done in the future by performing a Ljung-Box test.
Next in the code, we standardized the data in order to ensure that the different units used by each variable would not influence the nowcast disproportionately. This was done on each training and testing split, using the scale from the training split. On this transformed data, we obtained a correlation matrix to identify possibly multicollinearity within the exogenous variables. We found that ’Auto Gas’ was highly correlated with ’Petroleum Coal’. From domain knowledge, we knew that petroleum and coal production was linked to higher SO2 emissions, so ’Auto Gas’ was the variable that was dropped to reduce redundant information. We generated a new correlation matrix after dropping ’Auto Gas’.
For the following steps, we explored two versions of our data. The first of which was the full dataset, the second of which was truncated on Q1 of 2008, after which SO2 data levels off, becoming nearly constant with a slight seasonal pattern. The truncated dataset enabled us to explore model performance on test data that was more consistent with the training set.
For the untruncated dataset, training data spanned from Q1 of 1980 to Q4 of 2014. Testing data spanned from Q1 of 2015 through Q4 of 2023. For the truncated dataset, training data spanned from Q1 of 1980 to Q4 of 2003. Testing data spanned from Q1 of 2004 through Q4 of 2007.
For each of these datasets, we used SARIMAX, SARIMA, and average nowcasting models to impute the SO2 testing datasets. The SARIMAX and SARIMA models were tuned using rolling- window cross-validation, where MAE was the error metric of interest. Window sizes ranged from Q1 of 1981 to the end of the training set. Order and seasonal order parameters were explored using a grid search, where the rolling-average of MAE was calculated over all window sizes for each parameter combination. The parameter combination yielding the lowest average MAE was selected. The rolling-average window was used in order to ensure that the training and testing datasets had contiguous sequences of time-series data, and not random observations. This all was also done for the average model without any parameter tuning. In future work, we suggest that while performing cross-validation, each training and test split be transformed individually to prevent data leakage.
After the models were tuned, they were trained on the training datasets to nowcast the testing datasets. For both the untruncated and truncated versions, we produced figures that included nowcast plots, tables of the MAE, RMSE, and MASE error metrics, and plots of MAE as a function of window size. Feature coefficients were printed for the SARIMAX models.
