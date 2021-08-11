from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import metrics
from sklearn import tree
from sklearn.linear_model import LogisticRegression

import graphviz
from matplotlib import pyplot

import numpy as np

from sklearn.model_selection import train_test_split
import pandas as pd

x = pd.read_excel("data_imputed.xlsx")
y = x.pop("Class").values

x = x.drop("File", 1)
x = x.drop("Hakim Ketua", 1)
x = x.drop("Hakim Anggota 1", 1)
x = x.drop("Hakim Anggota 2", 1)
x = x.drop("Unnamed: 0", 1)
x = x.drop("Gender Ketua", 1)
x = x.drop("Gender Anggota 1", 1)
x = x.drop("Gender Anggota 2", 1)
x = x.drop("DJP Ketua", 1)
x = x.drop("DJP Anggota 1", 1)
x = x.drop("DJP Anggota 2", 1)

majelis = pd.get_dummies(x["Majelis"], prefix='Majelis')

x = pd.concat([x, majelis], axis=1, join='inner')
x = x.drop("Majelis", 1)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

clf1 = MultinomialNB()
clf2 = svm.SVC(probability=True, random_state=0)
clf3 = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
clf4 = AdaBoostClassifier()
clf5 = tree.DecisionTreeClassifier()
clf6 = LogisticRegression(random_state=0)


def returnClassReport(clf, Xtr, Ytr, Xts, Yts):
    clf.fit(Xtr, Ytr)
    predicted = clf.predict(Xts)
    print(metrics.classification_report(Yts, predicted))

print("Multinomial NB - Feature Based")
returnClassReport(clf1, X_train, y_train, X_test, y_test)

print("SVM - Feature Based")
returnClassReport(clf2, X_train, y_train, X_test, y_test)

print("Random Forest - Feature Based")
returnClassReport(clf3, X_train, y_train, X_test, y_test)

print("AdaBoost - Feature Based")
returnClassReport(clf4, X_train, y_train, X_test, y_test)

print("Decision Tree - Feature Based")
returnClassReport(clf5, X_train, y_train, X_test, y_test)

print("Logistic Regression - Feature Based")
returnClassReport(clf6, X_train, y_train, X_test, y_test)


# Visualisasikan Decision Tree
dot_data = tree.export_graphviz(clf5, 
								out_file=None, 
                                feature_names=list(x.columns),  
                   				class_names=[str(s) for s in np.unique(y)],
                                filled=True)

# Draw graph
graph = graphviz.Source(dot_data, format="png") 
graph.render("decision_tree_feature_based")

# Dram importance
importance = clf5.feature_importances_

features = list(x.columns)
# summarize feature importance
for i,v in enumerate(importance):
    print('Feature: %0s, Score: %.5f' % (features[i],v))

# plot feature importance
pyplot.bar([features[x] for x in range(len(importance))], importance)
pyplot.show()


    