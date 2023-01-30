import pandas as pd

df = pd.read_csv('aapl.us.txt')
df.head()

df = df[-1825:] #fix time: refer to chart, fix period: 30, 35

#data preprocessing

#We parse the date to the correct format
df['Date'] = pd.to_datetime(df['Date'])
#df.info()

#UNcomment if you want to exclude those before 2000.
#df = df[df['Date'].dt.year >= 2000]


#creating another date column for month, year and quarter so we can 'groupby' later
df['month'] = df['Date'].dt.to_period("M")
df['year'] = df['Date'].dt.to_period("Y")
df['quarter'] = df['Date'].dt.quarter

#df for Monthly
df_month = df.groupby(['month']).agg(
    mean_open = pd.NamedAgg(column='Open', aggfunc='mean'),
    mean_high = pd.NamedAgg(column='High', aggfunc='mean'),
    mean_low = pd.NamedAgg(column='Low', aggfunc='mean'),
    mean_close = pd.NamedAgg(column='Close', aggfunc='mean'),
    mean_volume = pd.NamedAgg(column='Volume', aggfunc='mean')
)

#df for Quarterly 
df_quarter = df.groupby(['year', 'quarter']).agg(
    mean_open = pd.NamedAgg(column='Open', aggfunc='mean'),
    mean_high = pd.NamedAgg(column='High', aggfunc='mean'),
    mean_low = pd.NamedAgg(column='Low', aggfunc='mean'),
    mean_close = pd.NamedAgg(column='Close', aggfunc='mean'),
    mean_volume = pd.NamedAgg(column='Volume', aggfunc='mean')
)

df = df #df_month, df_quarter
attribute = 'Close' #mean_close or Close
dropMe =['Close', 'Open', 'High', 'Low', 'Volume', 'OpenInt']
dropMe2 =['mean_close', 'mean_open', 'mean_high', 'mean_low', 'mean_volume']
drop = dropMe


#split into train and validation
index = int(len(df)*.7)
train = df[:index]
test = df[index:]
print(train)
x_train = train.drop(drop, axis=1)
x_train['Date'] = x_train.index
y_train = train[attribute]
x_test = test.drop(drop, axis=1)
x_test['Date'] = x_test.index
y_test = test[attribute]


#implement linear regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
x_train = x_train.drop([ 'month', 'quarter', 'year'], axis = True)
x_test = x_test.drop([ 'month', 'quarter', 'year'], axis = True)
model.fit(x_train,y_train)

#importing libraries
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

#scaling data
x_train_scaled = scaler.fit_transform(x_train)
x_train = pd.DataFrame(x_train_scaled)
x_test_scaled = scaler.fit_transform(x_test)
x_test = pd.DataFrame(x_test_scaled)

#using gridsearch to find the best parameter
params = {'n_neighbors':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,1]}
knn = neighbors.KNeighborsRegressor()
model = GridSearchCV(knn, params, cv=10)

#fit the model and make predictions
model.fit(x_train,y_train)
preds = model.predict(x_test)

print(model.n_splits_)
print(model.best_params_)

print(model.cv_results_.keys())
def printAll():
  for k, v in model.cv_results_.items():
    print(k)
    print(v)
#printAll()


#import required packages
from sklearn import neighbors
from sklearn.metrics import mean_squared_error 
from math import sqrt
import matplotlib.pyplot as plt

rmse_val = [] #to store rmse values for different k
for K in range(20):
    K = K+1
    model = neighbors.KNeighborsRegressor(n_neighbors = K)

    model.fit(x_train, y_train)  #fit the model
    pred=model.predict(x_test) #make prediction on test set
    error = sqrt(mean_squared_error(y_test,pred)) #calculate rmse
    rmse_val.append(error) #store rmse values
    print('RMSE value for k= ' , K , 'is:', error)

#plotting the rmse values against k values
curve = pd.DataFrame(rmse_val) #elbow curve 
curve.plot()