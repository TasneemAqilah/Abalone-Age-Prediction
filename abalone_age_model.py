# -*- coding: utf-8 -*-
"""Abalone age model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1quPU6-v5J1LZjaibx7QItmDttAlh_k2H

# Data Description


Predicting the age of abalone from physical measurements. The age of abalone is determined by cutting the shell through the cone, staining it, and counting the number of rings through a microscope -- a boring and time-consuming task. Other measurements, which are easier to obtain, are used to predict the age. Further information, such as weather patterns and location (hence food availability) may be required to solve the problem.

From the original data examples with missing values were removed (the majority having the predicted value missing), and the ranges of the continuous values have been scaled for use with an ANN (by dividing by 200).

# Attribute Information:

Given is the attribute name, attribute type, the measurement unit and a brief description. The number of rings is the value to predict: either as a continuous value or as a classification problem.

Name / Data Type / Measurement Unit / Description
-----------------------------

Sex / nominal / -- / M, F, and I (infant)

Length / continuous / mm / Longest shell measurement

Diameter	/ continuous / mm / perpendicular to length

Height / continuous / mm / with meat in shell

Whole weight / continuous / grams / whole abalone

Shucked weight / continuous	/ grams / weight of meat

Viscera weight / continuous / grams / gut weight (after bleeding)

Shell weight / continuous / grams / after being dried

Rings / integer / -- / +1.5 gives the age in years

# import libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

df = pd.read_csv('abalone.csv')

df.head()

df.describe()

df['age'] = df['Rings']+1.5
df = df.drop('Rings', axis = 1)

"""# EDA"""

# Check for missing values
df.isnull().sum()

df.describe()

"""The minimum height value is 0.00 this is most likely an error made.(noise) Probe the data frame further to identify the noise."""

# Condition to identify the noise
condition = df['Height'] == 0

# Use the condition to filter the DataFrame and extract the rows
rows_with_height_zero = df[condition]

# Display the filtered rows
print(rows_with_height_zero)
print("\nRows where height is zero:", rows_with_height_zero.value_counts().sum())

df.info()

"""Pairplot"""

pp = sns.pairplot(df, hue='Sex', markers=["o", "s", "D"], corner=True)

# Iterate over the axes object safely
for ax in pp.axes.flatten():
    if ax is not None:
        # Set label sizes
        ax.set_xlabel(ax.get_xlabel(), fontsize=16)
        ax.set_ylabel(ax.get_ylabel(), fontsize=16)

        # Set tick label sizes
        ax.tick_params(axis='both', which='major', labelsize=11)

# Remove any existing automatic legends created by seaborn
pp._legend.remove()

# Add a custom single legend
handles = pp._legend_data.values()
labels = pp._legend_data.keys()
legend = pp.figure.legend(handles=handles, labels=labels, title='Sex', loc='right', fontsize=16, title_fontsize=17)

plt.show()

"""Plot the distribution for individual features.
Although this can be seen in the pairplot, this is done to show the plots clearer in the presentation.
"""

# Set up matplotlib figure with subplots
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 10))

# Plot density plots for 'Length'
sns.kdeplot(data=df, x='Length', hue='Sex', fill=True, common_norm=False, ax=axes[0, 0])
axes[0, 0].set_title('Density Plot for Length')

# Plot density plots for 'Diameter'
sns.kdeplot(data=df, x='Diameter', hue='Sex', fill=True, common_norm=False, ax=axes[0, 1])
axes[0, 1].set_title('Density Plot for Diameter')

# Plot density plots for 'Height'
sns.kdeplot(data=df, x='Height', hue='Sex', fill=True, common_norm=False, ax=axes[1, 0])
axes[1, 0].set_title('Density Plot for Height')

# Plot density plots for 'Whole weight'
sns.kdeplot(data=df, x='Whole weight', hue='Sex', fill=True, common_norm=False, ax=axes[1, 1])
axes[1, 1].set_title('Density Plot for Whole Weight')

# Plot density plots for 'Shucked weight'
sns.kdeplot(data=df, x='Shucked weight', hue='Sex', fill=True, common_norm=False, ax=axes[2, 0])
axes[2, 0].set_title('Density Plot for Shucked Weight')

# Plot density plots for 'Viscera weight'
sns.kdeplot(data=df, x='Viscera weight', hue='Sex', fill=True, common_norm=False, ax=axes[2, 1])
axes[2, 1].set_title('Density Plot for Viscera Weight')

# Plot density plots for 'Shell weight'
sns.kdeplot(data=df, x='Shell weight', hue='Sex', fill=True, common_norm=False, ax=axes[3, 0])
axes[3, 0].set_title('Density Plot for Shell Weight')

# Plot density plots for 'Age'
sns.kdeplot(data=df, x='age', hue='Sex', fill=True, common_norm=False, ax=axes[3, 1])
axes[3, 1].set_title('Density Plot for Age')

# Adjust layout for better viewing
plt.tight_layout()
plt.show()

"""Plot the distribution of our target feature (Age)"""

plt.figure(figsize=(12, 6))
sns.countplot(x='age', data=df, palette='Dark2')
plt.xticks(rotation=45)  # Rotate labels to make them more readable
plt.title('Distribution of Age')
plt.show()

"""The distribution looks to be right-skewed with the mode at age 10.5

Plot a boxplot for age. This shows the majority age range (9.5 to 12.5)
"""

plt.style.use('ggplot')  # Use ggplot style
plt.figure(figsize=(6, 12))
sns.boxplot(y='age', data=df)
plt.title('Age Boxplot')
plt.ylabel('Age')
plt.show()

"""Calculate the proportion of ages from 9.5 to 12.5"""

majorityAge = ((df["age"]>=9.5) & (df["age"]<=12.5))
ageProportion = majorityAge.sum()/df["age"].count()
print("Porportion of ages from 9.5 to 12.5:", ageProportion.round(2))

"""Separate the features into numerical and categorical. Then, plot the correlation matrix."""

numerical_val = df.select_dtypes(include=['int64', 'float64']).columns
categorical_val = df.select_dtypes(include=['object']).columns
col_except_rings = ['Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight']

numerical_val

categorical_val

corr = df[numerical_val].corr()

# Mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

plt.figure(figsize=(20,7))

# Heatmap of correlation matrix
sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, cbar_kws={"shrink": .8})

plt.show()

"""**Key insights:**

- Physical measurements have strong positive correlations with each other (0.77 to 0.99)

- Moderate positive correlations between **most** phyiscal measurements (Length, Diameter, Height, Whole weight, Viscera weight, Shell weight) and Age (0.50 to 0.63)

- Weak positive correlation between Shucked weight and Age (0.42)

# Data Preprocessing

## Handling Outliers

Using boxplot to see the outliers in numerical features
"""

# Define the number of columns for subplots
num_cols = 2

num_rows = 7
# Create subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(14, 10))

# Flatten the axes array to iterate over the features
axes = axes.flatten()

# Iterate over each feature
for i, feature in enumerate(numerical_val):
    if i < len(numerical_val) - 1:
        # Plot histogram with KDE on the left side
        sns.histplot(df[feature], kde=True, ax=axes[i*num_cols])
        axes[i*num_cols].set_title(f'{feature} Distribution')
        axes[i*num_cols].set_xlabel('')
        axes[i*num_cols].set_ylabel('')

        # Plot boxplot on the right side
        sns.boxplot(x=df[feature], ax=axes[i*num_cols+1])
        axes[i*num_cols+1].set_title(f'{feature} Boxplot')
        axes[i*num_cols+1].set_xlabel('')
        axes[i*num_cols+1].set_ylabel('')

# Add a title for the entire subplot grid
fig.suptitle('Distribution of Features Before Cleaning Outliers', fontsize=16)

# Adjust layout
plt.tight_layout()
plt.show()

"""There are multiple ways to handle outliers:
1.   Winsorizing - Replace outliers with IQR upper and lowerbound values
2.   Averaging - Replace outliers with mean, median or mode values
3.   Removing - remove all outlier datas

After experimenting with all methods, removing provide the best results for all models.


"""

def detect_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = (data < lower_bound) | (data > upper_bound)
    return outliers

cleaned_df_train = df.copy()  # Make a copy of the original DataFrame

for col in col_except_rings:
    # Detect outliers using the IQR method for the current column
    outliers_mask = detect_outliers_iqr(cleaned_df_train[col])

    # Remove outliers from the cleaned DataFrame
    cleaned_df_train = cleaned_df_train[~outliers_mask]

cleaned_df_train.reset_index(drop=True, inplace=True)

"""Distribution after cleaning of data"""

# Define the number of columns for subplots
num_cols = 2

num_rows = 7
# Create subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(14, 10))

# Flatten the axes array to iterate over the features
axes = axes.flatten()

# Iterate over each feature
for i, feature in enumerate(numerical_val):
    if i < len(numerical_val) - 1:
        # Plot histogram with KDE on the left side
        sns.histplot(cleaned_df_train[feature], kde=True, ax=axes[i*num_cols])
        axes[i*num_cols].set_title(f'{feature} Distribution')
        axes[i*num_cols].set_xlabel('')
        axes[i*num_cols].set_ylabel('')

        # Plot boxplot on the right side
        sns.boxplot(x=cleaned_df_train[feature], ax=axes[i*num_cols+1])
        axes[i*num_cols+1].set_title(f'{feature} Boxplot')
        axes[i*num_cols+1].set_xlabel('')
        axes[i*num_cols+1].set_ylabel('')

# Add a title for the entire subplot grid
fig.suptitle('Distribution of Features After Cleaning Outliers', fontsize=16)

# Adjust layout
plt.tight_layout()
plt.show()

cleaned_df_train.info()

"""## PCA

As all numerical attributes has high correlation with each other, except for the target attribute, there present multicollinearity within the dataset.

To check whether the multicollinearity will affect our model prediction, we will experiment using PCA on the cleaned dataset. PCA will create new uncorrelated components from the original features and also allow for dimensionality reduction since we captured most of the information in the dataset with the least amount of principle components.
"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

feature_matrix = cleaned_df_train.iloc[:, 1:-1]

#feature_matrix = pd.get_dummies(feature_matrix)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(feature_matrix)

pca = PCA()
pca.fit(X_scaled)

# Explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_var_exp = np.cumsum(explained_variance_ratio)

# Plot the explained variance ratio
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(explained_variance_ratio) + 1), cumulative_var_exp, marker='o')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Explained Variance by Component')
plt.grid(True)
plt.show()

"""Using the elbow method, it seems that the increase in explained variance slowed down after 5 components. Therefore, we will choose 5 Principle Components for our analysis."""

n_components = 5
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X_scaled)

"""Since, we cannot view 5-dimensional pca scatter plot, we will analyse using only PC1 and PC2, which accounts for the highest explained variance. Based on the graph, we can see some clustering, with 1 big clusters and many smaller clusters."""

# Create a DataFrame for the principal components
principalDf = pd.DataFrame(data = X_pca, columns = ['principal component 1', 'principal component 2', 'principal component 3', 'principal component 4', 'principal component 5'])

# Visualize the first two principal components
plt.figure(figsize=(8, 6))
plt.scatter(principalDf['principal component 1'], principalDf['principal component 2'])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA Scatter Plot')
plt.show()

#add sex into principalDF
df_combined = pd.concat([principalDf, cleaned_df_train.select_dtypes(include=['object'])], axis=1)

df_combined.info()

"""# Feature Selection and Standardization

Instead of using only 1 dataset to train and test, we will use 3 different dataset to train and test. Reason being:


1.   As observed, after the removal of outliers dataset, the correlation of predictor attribute and the target attribute decreases. Hence, it will be useful to have the original dataset as benchmark.
2.   As observed, there are multicollinearity within the dataset, therefore, we should test whether having no correlation between predictor attributes improve the model.

Other than PCA dataset which has been scaled previously, the other dataset will be normalised to improve model performance. Additionally, a random seed has been added to keep performance consistent for testing.
"""

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score

random_seed = 42
np.random.seed(random_seed)

standardScale = StandardScaler()

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score

random_seed = 42
np.random.seed(random_seed)

standardScale = StandardScaler()

"""Original dataset"""

df = pd.get_dummies(df)

X1 = df.drop('age', axis = 1)
y1 = df['age']

X_scaled1 = standardScale.fit_transform(X1)

X_train1, X_test1, y_train1, y_test1 = train_test_split(X_scaled1, y1, test_size=0.2, random_state=random_seed)

"""Cleaned dataset"""

# encode sex handling
cleaned_df_train_encoded = pd.get_dummies(cleaned_df_train)

X2 = cleaned_df_train_encoded.drop('age', axis = 1)
y2 = cleaned_df_train_encoded['age']

X_scaled2 = standardScale.fit_transform(X2)

X_train2, X_test2, y_train2, y_test2 = train_test_split(X_scaled2, y2, test_size=0.2, random_state=random_seed)

"""PCA dataset"""

X3 = pd.get_dummies(df_combined)
y3 = cleaned_df_train['age']

X_train3, X_test3, y_train3, y_test3 = train_test_split(X3, y3, test_size=0.2, random_state=random_seed)

"""# Model Selection"""

from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score
def model_evaluation(model, X_train, y_train, X_test, y_test, name):
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print('\nEvaluation for: %s\n'%name)

    mse_train = mean_squared_error(y_train, y_train_pred)
    print('Mean Squared error of training set: %.2f'%mse_train)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    print('Mean Absolute error of training set: %.2f'%mae_train)
    r2_train = r2_score(y_train, y_train_pred)
    print('R2 Score of training set: %.2f'%r2_train)

    print()

    mse_test = mean_squared_error(y_test, y_test_pred)
    print('Mean Squared error of testing set: %.2f'%mse_test)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    print('Mean Absolute error of testing set: %.2f'%mae_test)
    r2_test = r2_score(y_test, y_test_pred)
    print('R2 Score of testing set: %.2f'%r2_test)

"""# 1) Linear Regression"""

from sklearn.linear_model import LinearRegression

model_evaluation(LinearRegression(), X_train1, y_train1, X_test1, y_test1,  'Linear Regression Original Dataset')
model_evaluation(LinearRegression(), X_train2, y_train2, X_test2, y_test2,  'Linear Regression Cleaned Dataset')
model_evaluation(LinearRegression(), X_train3, y_train3, X_test3, y_test3,  'Linear Regression PCA Dataset')

"""# 2) Ridge"""

from sklearn.linear_model import Ridge

model_evaluation(Ridge(), X_train1, y_train1, X_test1, y_test1,  'Ridge Original Dataset')
model_evaluation(Ridge(), X_train2, y_train2, X_test2, y_test2,  'Ridge Cleaned Dataset')
model_evaluation(Ridge(), X_train3, y_train3, X_test3, y_test3,  'Ridge PCA Dataset')

"""# 3) Support Vector Regression"""

from sklearn.svm import SVR

"""10min per model total 25min"""

model_evaluation(SVR(kernel = 'linear'), X_train1, y_train1, X_test1, y_test1,  'SVR Original Dataset')
model_evaluation(SVR(kernel = 'linear'), X_train2, y_train2, X_test2, y_test2,  'SVR Cleaned Dataset')
model_evaluation(SVR(kernel = 'linear'), X_train3, y_train3, X_test3, y_test3,  'SVR PCA Dataset')

"""#4) Decision Tree Regression"""

from sklearn.tree import DecisionTreeRegressor

model_evaluation(DecisionTreeRegressor(random_state=42), X_train1, y_train1, X_test1, y_test1,  'DecisionTreeRegressor Original Dataset')
model_evaluation(DecisionTreeRegressor(random_state=42), X_train2, y_train2, X_test2, y_test2,  'DecisionTreeRegressor Cleaned Dataset')
model_evaluation(DecisionTreeRegressor(random_state=42), X_train3, y_train3, X_test3, y_test3,  'DecisionTreeRegressor PCA Dataset')

"""# 5) Random Forest Regression"""

from sklearn.ensemble import RandomForestRegressor

model_evaluation(RandomForestRegressor(), X_train1, y_train1, X_test1, y_test1,  'RandomForestRegressor Original Dataset')
model_evaluation(RandomForestRegressor(), X_train2, y_train2, X_test2, y_test2,  'RandomForestRegressor Cleaned Dataset')
model_evaluation(RandomForestRegressor(), X_train3, y_train3, X_test3, y_test3,  'RandomForestRegressor PCA Dataset')

"""# 6) Gradient Boosting Regression"""

from sklearn.ensemble import GradientBoostingRegressor

model_evaluation(GradientBoostingRegressor(), X_train1, y_train1, X_test1, y_test1,  'GradientBoostingRegressor Original Dataset')
model_evaluation(GradientBoostingRegressor(), X_train2, y_train2, X_test2, y_test2,  'GradientBoostingRegressor Cleaned Dataset')
model_evaluation(GradientBoostingRegressor(), X_train3, y_train3, X_test3, y_test3,  'GradientBoostingRegressor PCA Dataset')

from sklearn.neighbors import KNeighborsRegressor

model_evaluation(KNeighborsRegressor(n_neighbors =4 ), X_train1, y_train1, X_test1, y_test1,  'KNN Original Dataset')
model_evaluation(KNeighborsRegressor(n_neighbors =4 ), X_train2, y_train2, X_test2, y_test2,  'KNN Cleaned Dataset')
model_evaluation(KNeighborsRegressor(n_neighbors =4 ), X_train3, y_train3, X_test3, y_test3,  'KNN PCA Dataset')

"""#8) Artificial Neural Network

"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import Input

def ann_model_evaluation(X_train, y_train, X_test, y_test, name):
    # Build the ANN
    ann_model = Sequential()

        # Input layer
    ann_model.add(Input(shape=(X_train.shape[1],)))

    # First hidden layer
    ann_model.add(Dense(64, activation='relu'))

    # Second hidden layer
    ann_model.add(Dense(32, activation='relu'))

    # Output layer
    ann_model.add(Dense(1, activation='linear'))

    # Compile the model
    ann_model.compile(optimizer='adam', loss='mse')

    # Train the model
    ann_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=0)

    y_train_pred = ann_model.predict(X_train)
    y_test_pred = ann_model.predict(X_test)

    print('Evaluation for: %s\n'%name)

    mse_train = mean_squared_error(y_train, y_train_pred)
    print('Mean Squared error of training set: %.2f'%mse_train)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    print('Mean Absolute error of training set: %.2f'%mae_train)
    r2_train = r2_score(y_train, y_train_pred)
    print('R2 Score of training set: %.2f'%r2_train)

    print()

    mse_test = mean_squared_error(y_test, y_test_pred)
    print('Mean Squared error of testing set: %.2f'%mse_test)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    print('Mean Absolute error of testing set: %.2f'%mae_test)
    r2_test = r2_score(y_test, y_test_pred)
    print('R2 Score of testing set: %.2f'%r2_test)

ann_model_evaluation(X_train1, y_train1, X_test1, y_test1,  'ANN Original Dataset')
ann_model_evaluation(X_train2, y_train2, X_test2, y_test2,  'ANN Cleaned Dataset')
ann_model_evaluation(X_train3, y_train3, X_test3, y_test3,  'ANN PCA Dataset')

"""# Hyperparameter Tunning Using GridSearchCV"""

from sklearn.model_selection import  GridSearchCV

#Hyperparameter tunning
# Hyperparameter tuning using GridSearchCV
def hyperparameter_tuning(model, param_grid):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='r2', cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_
    return best_params, best_score

"""Linear Regression does not have hyperparameters"""

# Linear Regression

#initialise the model
lr = LinearRegression()

# fit the model to the training data
lr.fit(X_train, y_train)

#predict the target values for the training data
y_train_pred = lr.predict(X_train)

#predict the target values for the test data
y_test_pred = lr.predict(X_test)

# calculate and print the R2 score for the test data
# R2 score indicates how well the model's predictions match the actual target values
# ranges from 0 to 1, 1 means perfect prediction and 0 means no better than the mean of the target variable
print(f'Linear Regression R2 Score: {r2_score(y_test, y_test_pred)}')

# Calculate and print the Mean Squared Error for the test data
mse_test = mean_squared_error(y_test, y_test_pred)
print(f'Linear Regression Mean Squared Error: {mse_test:.2f}')

# Ridge Regression
ridge_params = {
    'alpha': [0.01, 0.1, 1, 10, 100],
    'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
}

ridge_best_params, ridge_best_score = hyperparameter_tuning(Ridge(random_state=42), ridge_params)

# Display the best parameters and best score
print(f'Best Ridge Params: {ridge_best_params}, Best Ridge Score: {ridge_best_score}')

# Create the Ridge model with the best parameters
ridge_mod = Ridge(**ridge_best_params, random_state=42)

# Train the model with the training data
ridge_mod.fit(X_train, y_train)

# Make predictions on the test data
ridge_model_pred = ridge_mod.predict(X_test)

# Evaluate the model's performance
ridge_r2 = ridge_mod.score(X_test, y_test)
ridge_mse = mean_squared_error(y_test, ridge_model_pred)

print(f'Ridge Regression R2 Score: {ridge_r2:.2f}')
print(f'Ridge Regression Mean Squared Error: {ridge_mse:.2f}')

# Support Vector Regressor

svr_params = {'kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 'C': [0.1, 1, 10, 100], 'gamma': ['scale', 'auto']}
svr_best_params, svr_best_score = hyperparameter_tuning(SVR(), svr_params)

# Display the best parameters and best score
print(f'Best SVR Params: {svr_best_params}, Best SVR Score: {svr_best_score}')

#create the SVR model with the best parameters
svr_mod = SVR(**svr_best_params)

#train the model with the training data
svr_mod.fit(X_train, y_train)

# Make predictions on the test data
svr_model_pred = svr_mod.predict(X_test)

# Evaluate the model's performance
svr_r2 = svr_mod.score(X_test, y_test)
svr_mse = mean_squared_error(y_test, svr_model_pred)

print(f'Support Vector Regression R2 Score: {svr_r2:.2f}')
print(f'Support Vector Regression Mean Squared Error: {svr_mse:.2f}')

# Random Forest Regressor
rf_params = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20, 30], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}
rf_best_params, rf_best_score = hyperparameter_tuning(RandomForestRegressor(random_state=42), rf_params)

# Display the best parameters and best score
print(f'Best RF Params: {rf_best_params}, Best RF Score: {rf_best_score}')

#create the RF model with the best parameters
rf_mod = RandomForestRegressor(**rf_best_params, random_state=42)

#train the model with the training data
rf_mod.fit(X_train, y_train)

# Make predictions on the test data
rf_model_pred = rf_mod.predict(X_test)

# Evaluate the model's performance
rf_r2 = rf_mod.score(X_test, y_test)
rf_mse = mean_squared_error(y_test, rf_model_pred)

print(f'Random Forest Regression R2 Score: {rf_r2:.2f}')
print(f'Random Forest Regression Mean Squared Error: {rf_mse:.2f}')

# Gradient Boosting Regressor
gbr_params = {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.2], 'max_depth': [3, 4, 5]}
gbr_best_params, gbr_best_score = hyperparameter_tuning(GradientBoostingRegressor(random_state=42), gbr_params)

# Display the best parameters and best score
print(f'Best GBR Params: {gbr_best_params}, Best GBR Score: {gbr_best_score}')

#create the GBR model with the best parameters
gbr_mod = GradientBoostingRegressor(**gbr_best_params, random_state=42)

#train the model with the training data
gbr_mod.fit(X_train2, y_train2)

#Make predictions on the test data
gbr_model_pred = gbr_mod.predict(X_test2)

# Evaluate the model's performance
gbr_r2 = gbr_mod.score(X_test2, y_test2)
gbr_mse = mean_squared_error(y_test2, gbr_model_pred)

print(f'Gradient Boosting Regression R2 Score: {gbr_r2:.2f}')
print(f'Gradient Boosting Regression Mean Squared Error: {gbr_mse:.2f}')

# K-Nearest Neighbors Regressor
knn_params = {'n_neighbors': [3, 5, 7, 9], 'weights': ['uniform', 'distance'], 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
knn_best_params, knn_best_score = hyperparameter_tuning(KNeighborsRegressor(), knn_params)

# Display the best parameters and best score
print(f'Best KNN Params: {knn_best_params}, Best KNN Score: {knn_best_score}')

#create the KNN model with the best parameters
knn_mod = KNeighborsRegressor(**knn_best_params)

#train the model with the training data
knn_mod.fit(X_train, y_train)

# Make predictions on the test data
knn_model_pred = knn_mod.predict(X_test)

# Evaluate the model's performance
knn_r2 = knn_mod.score(X_test, y_test)
knn_mse = mean_squared_error(y_test, knn_model_pred)

print(f'K-Nearest Neighbors Regression R2 Score: {knn_r2:.2f}')
print(f'K-Nearest Neighbors Regression Mean Squared Error: {knn_mse:.2f}')

!pip install keras-tuner

#Artificial Neural Network

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import Input
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import keras_tuner as kt

# Normalize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define a function to create the model
def build_model(hp):
    model = Sequential()
    model.add(Input(shape=(X_train_scaled.shape[1],)))

    # First hidden layer with variable number of units
    model.add(Dense(units=hp.Int('units', min_value=32, max_value=128, step=32), activation=hp.Choice('activation', values=['relu', 'tanh'])))
    model.add(Dropout(rate=hp.Float('dropout_rate', min_value=0.2, max_value=0.5, step=0.1)))

    # Second hidden layer with variable number of units
    model.add(Dense(units=hp.Int('units2', min_value=16, max_value=64, step=16), activation=hp.Choice('activation', values=['relu', 'tanh'])))
    model.add(Dropout(rate=hp.Float('dropout_rate', min_value=0.2, max_value=0.5, step=0.1)))

    # Output layer
    model.add(Dense(1, activation='linear'))

    model.compile(
        optimizer=hp.Choice('optimizer', values=['adam', 'rmsprop']),
        loss='mean_squared_error',
        metrics=['mean_squared_error']
    )
    return model

# Initialize KerasTuner
tuner = kt.RandomSearch(
    build_model,
    objective='val_mean_squared_error',
    max_trials=10,  # Increase the number of trials
    executions_per_trial=1,
    directory='my_dir',
    project_name='ann_tuning'
)

# Implement early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Perform hyperparameter search
tuner.search(X_train_scaled, y_train, epochs=100, validation_split=0.2, callbacks=[early_stopping])

# Retrieve the best hyperparameters and model
best_model = tuner.get_best_models(num_models=1)[0]
best_params = tuner.get_best_hyperparameters()[0]

print(f'Best Parameters: {best_params.values}')

# Train the best model
best_model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Predict using the best model
ann_model_pred_train = best_model.predict(X_train_scaled)
ann_model_pred_test = best_model.predict(X_test_scaled)

# Evaluate the best model
mse_train = mean_squared_error(y_train, ann_model_pred_train)
mae_train = mean_absolute_error(y_train, ann_model_pred_train)
r2_train = r2_score(y_train, ann_model_pred_train)

mse_test = mean_squared_error(y_test, ann_model_pred_test)
mae_test = mean_absolute_error(y_test, ann_model_pred_test)
r2_test = r2_score(y_test, ann_model_pred_test)

print(f'\nMean Squared error of training set: {mse_train:.2f}')
print(f'Mean Absolute error of training set: {mae_train:.2f}')
print(f'R2 Score of training set: {r2_train:.2f}')

print(f'\nMean Squared error of testing set: {mse_test:.2f}')
print(f'Mean Absolute error of testing set: {mae_test:.2f}')
print(f'R2 Score of testing set: {r2_test:.2f}')

#Decision Tree Regressor
# Define the hyperparameter grid
param_grid = {
    'max_depth': [None, 10, 20, 30, 40, 50],  # Maximum depth of the tree
    'min_samples_split': [2, 10, 20],         # Minimum samples required to split an internal node
    'min_samples_leaf': [1, 5, 10]            # Minimum samples required to be at a leaf node
}

#initialize GridSearchCV with DecisionTreeRegressor
grid = GridSearchCV(estimator=DecisionTreeRegressor(random_state=42),
                    param_grid=param_grid,
                    scoring='r2',  # Use R2 as the scoring metric
                    cv=5,          # 5-fold cross-validation
                    n_jobs=-1)     # Use all available cores

#fit GridSearchCV to the training data
grid_result = grid.fit(X_train, y_train)

#print the best parameters and best score
print(f'Best Parameters: {grid_result.best_params_}')
print(f'Best R2 Score: {grid_result.best_score_}')

#use the best estimator to predict on test data
best_dt = grid_result.best_estimator_
y_test_pred = best_dt.predict(X_test)

#evaluate the model's performance
best_test_mse = mean_squared_error(y_test, y_test_pred)
best_test_r2 = r2_score(y_test, y_test_pred)
print(f'Decision Tree Regression Mean Squared Error: {best_test_mse:.2f}')
print(f'Decision Tree Regression R2 Score: {best_test_r2:.2f}')

# Define performance metrics for each model
model_performance = {
    'Linear Regression (Tuned)': {'MSE': 4.46, 'R2': 0.549},
    'Ridge Regression (Tuned)': {'MSE': 4.46, 'R2': 0.55},
    'SVR (Tuned)': {'MSE': 4.42, 'R2': 0.55},
    'Decision Tree Regressor (Tuned)': {'MSE': 5.49, 'R2': 0.45},
    'Random Forest Regressor (Tuned)': {'MSE': 4.33, 'R2': 0.56},
    'K-Nearest Neighbors (Tuned)': {'MSE': 5.18, 'R2': 0.52},
    'Gradient Boosting Regressor (Tuned)': {'MSE': 4.55, 'R2': 0.54},
    'ANN (Tuned)': {'MSE': 4.29, 'R2': 0.57}
}

# Find the model with the highest R2 Score
best_model = max(model_performance, key=lambda x: model_performance[x]['R2'])
best_model_metrics = model_performance[best_model]

# Display the best model and its performance metrics
print(f'Best Model: {best_model}')
print(f'Mean Squared Error: {best_model_metrics["MSE"]:.2f}')
print(f'R2 Score: {best_model_metrics["R2"]:.2f}')

"""# In conclusion, The Artificial Neural Network (ANN) model (both untuned and tuned) shows the best performance with the highest R2 score of 0.57 and the lowest MSE around 4.22 to 4.29. This indicates that the ANN model is the best choice for predicting abalone age in this context."""