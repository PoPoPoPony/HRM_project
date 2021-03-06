from numpy.core.fromnumeric import mean
from sklearn.utils import multiclass
from model import SVM_1, RFclassifier
import pandas as pd
from sklearn.model_selection import KFold, cross_validate
from sklearn.metrics import make_scorer, recall_score, roc_auc_score, f1_score, accuracy_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import make_pipeline

def validation(N, df, model):
    kf = KFold(n_splits=N, random_state=100, shuffle=True)
    scoring = {
        'acc': make_scorer(accuracy_score),
        'recall': make_scorer(recall_score, average='macro'),
        # 'roc and auc': make_scorer(roc_auc_score, multi_class='ovr'),
        'f1': make_scorer(f1_score, average='macro')
    }
    x_data = df.iloc[:,1:-1]
    y_data = df.iloc[:,-1]
    print(x_data.shape)
    clf = make_pipeline(MinMaxScaler(), model)
    results = cross_validate(
        estimator=clf,
        X=x_data,
        y=y_data,
        cv=kf,
        scoring=scoring,
        #return_estimator=True # this arg is for saving svm model
    )
    
    '''
    for train_idx, test_idx in kf.split(df.iloc[:, :-1]):
        X_train, X_test = df.iloc[train_idx, :-1], df.iloc[test_idx, :-1]
        y_train, y_test = df.iloc[train_idx, -1], df.iloc[test_idx, -1]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test, y_test)
    ''' 
    #print(results['estimator'])

    for i, j in results.items():
        print(i, mean(j))
    print("\n")


if __name__=='__main__':
    model = SVM_1()
    df = pd.read_csv('training_data/training_concat.csv', encoding='big5', low_memory=False)
    validation(3, df, model)
    



