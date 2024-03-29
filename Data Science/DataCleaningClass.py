import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
sns.set(style='darkgrid')

class DataCleaning:
    def data_info(self, data):
        cols, dtype, nulls, duplicates, uniques = [], [], [], [], []

        for col in data.columns:
            cols.append(col)
            dtype.append(data[col].dtype)
            nulls.append(data[col].isnull().sum())
            duplicates.append(data.duplicated().sum())
            uniques.append(data[col].nunique())

        df = pd.DataFrame(
            {'Column': cols, 'DType': dtype, 'no of Nulls': nulls, 'no of Uniques': uniques, 'Duplicated rows': duplicates})
        return df


    # __data=[]
    def split_data(self, data, categorical_threshold=10):
        numerical_data = data.select_dtypes(include=['number'])
        object_data = data.select_dtypes(include=['object'])
        unique_data = data.nunique()
        cat_cols = unique_data[unique_data <= categorical_threshold].index
        cont_cols = unique_data[unique_data > categorical_threshold].index
        return numerical_data, object_data, cat_cols, cont_cols

    # numerical_data, object_data, cat_cols, cont_cols = split_data(data, 10)

# NUMERICAL PLOTTING
    def columns_histplot(self, data):
        # data = numerical data
        c = 3
        r = math.ceil(len(data.columns)/c)
        plt.figure(figsize=(20,5*r))
        l = len(data.columns)
        for i in range(l):
            plt.subplot(r, c, i + 1)
            sns.histplot(data[data.columns[i]], bins=10, kde=True)
            plt.title(f'HistPlot of {data.columns[i]}', fontsize=14, color='darkblue')
            plt.xticks(rotation=45)
            plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()

    def columns_boxplot(self, data):
        # data = numerical_data
        l = len(data.columns)
        plt.figure(figsize=(20, 30))
        for i in range(l):
            plt.subplot(l, 1, i + 1)
            sns.boxplot(x=data[data.columns[i]])
            plt.title(f'BoxPlot of {data.columns[i]}', fontsize=22, color='darkblue')

        plt.tight_layout()
        plt.show()

# CATEGORICAL PLOTTING
    def columns_pie(self, data):
        # data = data[cat_cols]
        c = 3
        r = math.ceil(len(data.columns) / c)
        plt.figure(figsize=(100, 100))
        l = len(data.columns)
        for i in range(l):
            plt.subplot(r, c, i + 1)
            unique_values = data[data.columns[i]].unique()
            label = unique_values if not pd.isnull(unique_values).any() else unique_values[:-1]
            plt.pie(data[data.columns[i]].value_counts(normalize=True), autopct='%1.0f%%', labels=label,
                    textprops={'fontsize': 48})
            plt.title(f'Pie Chart of {data.columns[i]}', fontsize=64)
        plt.tight_layout()
        plt.show()


# CATEGORICAL PLOTTING WITH RESPECT TO CONTINUOUS TARGET
    def columns_barplot(self, data, target_data):
        # data = data[cat_cols]
        # target_data = the data of the target column if it is categorical
        l = len(data.columns)
        plt.figure(figsize=(10, 30))
        for i in range(l):
            plt.subplot(l, 1, i + 1)
            sns.barplot(x=data.columns[i], y=target_data)
            plt.title(f'BarPlot of {data.columns[i]} related to the {target_data.name}', fontsize=14, color='darkblue')

        plt.tight_layout()
        plt.show()

    def columns_countplot(self, data, target_data):
        # data = data[cat_cols]
        # target_data = the data of the target column if it is categorical
        c=3
        r=math.ceil(len(data.columns)/c)
        plt.figure(figsize=(20,5*r))
        l = len(data.columns)
        for i in range(l):
            plt.subplot(r, c, i + 1)
            sns.countplot(x = data[data.columns[i]], hue =target_data)
            plt.title(f'CountPlot of {data.columns[i]} with {target_data.name} as a hue ', fontsize=22, color='darkblue')
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()


# CONTINUOUS PLOTTING WITH RESPECT TO CONTINUOUS TARGET
    def columns_scatterplot(self, data, target_data):
        # data = data[cont_cols]
        # target_data = the data of the target column if it is continuous
        c = 3
        r = math.ceil(len(data.columns)/c)
        plt.figure(figsize=(20,5*r))
        l = len(data.columns)
        for i in range(l):
            plt.subplot(r, c, i + 1)
            sns.scatterplot(x = data[data.columns[i]], y =target_data)
            plt.title(f'ScatterPlot of {data.columns[i]} with {target_data.name}', fontsize=22, color='darkblue')
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def columns_lineplot(self, data, target_data):
        # data = data[cont_cols]
        # target_data = the data of the target column if it is continuous
        l = len(data.columns)
        plt.figure(figsize=(20, 30))
        for i in range(l):
            plt.subplot((l//2)+1, 2, i + 1)
            sns.lineplot(x=data[data.columns[i]],y=target_data)
            plt.title(f'Line Plot of {data.columns[i]} with {target_data.name}', fontsize=22, color='darkblue')

        plt.tight_layout()
        plt.show()




# DATA CLEANING
    def columns_fillna(data):
        for col in data.columns:
            if col in (data.select_dtypes(include=['number'])):
                data[col] = data[col].fillna(data[col].median())
            elif col in (data.select_dtypes(include=['object'])):
                data[col] = data[col].fillna(data[col].mode()[0])

        return data


    def columns_outlier(data, drop_categorical_outliers=False):
        for col in data.columns:
            if col in (data.select_dtypes(include=['number'])):
                q1, q3 = data[col].quantile([0.25, 0.75])
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outlier = (data[col] < lower) | (data[col] > upper)
                data = data[~outlier]

            elif col in (data.select_dtypes(include=['object']) and drop_categorical_outliers==True):
                for value in data[col].unique():
                    value_len = len(data[data[col]==value])
                    if value_len < len(data.columns):
                        data = data.drop(data[data[col]==value].index, axis=0)

            data.reset_index(drop=True, inplace=True)
        return data


    def columns_transformation(data):
        skewed_data = data.skew()
        right_skewed = skewed_data[skewed_data > 0.6]
        left_skewed = skewed_data[skewed_data < (-0.5)]
        for col in skewed_data.index:
            if col in right_skewed.index:  # right skewed --> log transformer
                tr = ColumnTransformer(transformers=[('lg', FunctionTransformer(np.log1p), [col])])
                tr_type = 'Log'
            elif col in left_skewed.index:  # left skewed --> square tranformer
                tr = ColumnTransformer(transformers=[('sq', FunctionTransformer(np.square), [col])])
                tr_type = 'Square'
            else:
                continue
            plt.figure(figsize=(15, 6))
            col_tr = pd.DataFrame(tr.fit_transform(data))
            skew_before = data[col].skew()
            skew_after = col_tr[0].skew()
            plt.subplot(1, 2, 1)
            plt.title(f"Distribution of {col} before Transformation", fontsize=15)
            sns.histplot(data[col], kde=True, color="red")

            data[col] = col_tr[0]
            plt.subplot(1, 2, 2)
            plt.title(f"Distribution of {col} after Transformation", fontsize=15)
            sns.histplot(data[col], bins=20, kde=True, legend=False)
            plt.xlabel(col)
            plt.show()
            print(
                f"Skewness was {round(skew_before, 2)} before & now it is {round(skew_after, 2)} after {tr_type} transformation.")

        return data

    def columns_lencoder(data):
        le = LabelEncoder()
        for col in data.columns:
            data[col] = le.fit_transform(data[col])
        return data

    def columns_drop(data, cols):
        # data = data
        # cols = list of columns you need to drop
        # -- do not forget to call the split function
        data = data.drop(columns = cols, axis=1)
        data = data.reset_index(drop=True)
        return data



