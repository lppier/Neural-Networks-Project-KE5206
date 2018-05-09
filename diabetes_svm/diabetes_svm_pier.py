import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
import os

# Load Data
os.chdir("/home/pier/Machine_Learning/KE5206NN/diabetes_svm")
dfs = pd.read_excel("data/diabetic_data.xlsx", sheet_name=None)
df = dfs['in']
df = df.iloc[:, 2:]
print(df.shape)

# Data Exploration
corr = df.corr()
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
plt.show()
df.describe()

df_numeric = df.select_dtypes(include=[np.number])

# drop missing values
df = df.replace('?', np.nan)
df = df.replace('Unknown/Invalid', np.nan)
print(df.columns[df.isnull().any()])
df.isnull().sum()
# df = df.dropna() # dangerous! dropped until left 1k plus rows

print(df.shape)
df = df.drop(columns=df.columns[df.nunique() == 1])  # drop columns which only have 1 category

to_num = ['time_in_hospital', 'num_lab_procedures', 'num_procedures',
          'num_medications', 'number_outpatient', 'number_emergency',
          'number_inpatient', 'number_diagnoses']

to_cat_codes = list(set(df.columns) - set(to_num))
df_test = df

# X_features = list(to_num)
# for c in to_cat_codes:
#     df_test[c + '_cat'] = df_test[c].cat.codes
#     X_features += [c + '_cat']
#
# X_features.remove('readmitted_cat')

obj_df = df.select_dtypes(include=['object']).copy()
obj_df.head()
df = df.fillna({'weight': df['weight'].value_counts().index[0]})
df = df.fillna({'payer_code': 'NOT_SPECIFIED', 'medical_specialty': 'NOT_SPECIFIED'})

# for col in list(obj_df.columns.values):
#     df[col] = df[col].astype('category')
df['age'] = df['age'].astype('category')
df['age'] = df['age'].cat.codes
df['weight'] = df['weight'].astype('category')
df['weight'] = df['weight'].cat.codes
df['readmitted'] = df['readmitted'].astype('category')
df['readmitted'] = df['readmitted'].cat.codes

# one hot the rest
column_names = list(df.select_dtypes(include=['object']).columns.values)
one_hot = pd.get_dummies(df.select_dtypes(include=['object']))
df = df.drop(column_names, axis=1)
df = df.join(one_hot)

df_x = df.loc[:, df.columns != 'readmitted']
df_y = df.loc[:, df.columns == 'readmitted']

X_train, X_test, y_train, y_test = train_test_split(
    df_x, df_y, test_size=0.3, random_state=42)

scaler = MinMaxScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train))
X_test = pd.DataFrame(scaler.transform(X_test))
clf = LinearSVC().fit(X_train, y_train)
print('training accuracy: {:.2f}'.format(clf.score(X_train, y_train)))
print('test accuracy: {:.2f}'.format(clf.score(X_test, y_test)))
