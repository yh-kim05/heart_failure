import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, accuracy_score
from sklearn.impute import SimpleImputer
from category_encoders import OrdinalEncoder, OneHotEncoder
from xgboost import XGBClassifier

raw_csv = pd.read_csv('/Users/yunheekim/codestates/Section3/project3/heart_900.csv')

train, test = train_test_split(raw_csv, train_size= 0.8, test_size=0.2)

def divide_dataset(df):

    target = 'HeartDisease'

    features = df.drop(columns = [target]).columns

    X = df[features]
    y = df[target]

    return X, y

X_train, y_train = divide_dataset(train)
X_test, y_test = divide_dataset(test)

def fit_model(X_train, y_train):

    pipe = make_pipeline(
        OrdinalEncoder(),
        SimpleImputer(),
        XGBClassifier()
    )

    dists = {
        'simpleimputer__strategy' : ['mean', 'median', 'most_frequent'],
        'xgbclassifier__n_estimator' : range(1, 500),
        'xgbclassifier__max_depth' : range(3, 20),
        'xgbclassifier__learning_rate' : [0.1, 0.2, 0.3],
        'xgbclassifier__min_child_weight' : range(0, 30)
    }

    clf = RandomizedSearchCV(
        pipe,
        param_distributions = dists,
        n_iter = 10,
        cv = 5,
        scoring = 'f1',
        n_jobs = -1
    )

    clf.fit(X_train, y_train)

    return clf

clf = fit_model(X_train, y_train)

y_test_pred = clf.best_estimator_.predict(X_test)

# test_x_dic = {'age' : 59,
#           'sex': 'M',
#           'ChestPainType' : 'ATA',
#           'RestingBP':140,
#           'Cholesterol': 289,
#           'FastingBS':  0,
#           'RestingECG':  'Normal',
#           'MaxHR' : 172,
#           'ExerciseAngina' : 'N',
#           'Oldpeak' : 0,
#           'ST_Slope' : 'Up'}
# test_x = pd.DataFrame(data = test_x_dic, )

test_x = pd.DataFrame([[40, 'M', 'ATA', 140, 289, 0, 'Normal', 172, 'N', 0, 'Up']] , columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'])

pred_y = clf.best_estimator_.predict(test_x)

print(f'{test_x} 은 예상이 {pred_y} 입니다.')

import pickle

with open('model.pkl', 'wb') as pickle_file:
    pickle.dump(clf.best_estimator_, pickle_file)

