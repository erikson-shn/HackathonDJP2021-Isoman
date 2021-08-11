import os
from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import metrics
from sklearn import tree
from sklearn.linear_model import LogisticRegression

def readStopword():
    fstopw = open('id.stopwords.02.01.2016.txt','r')
    stopw = set([w for w in fstopw])
    stopadd = ['karena','dia','adalah','jadi','yg','dan','ia','ini', 'di']
    for s in stopadd:
      stopw.add(s)
    # print(len(stopw))
    
    return stopw

def preprocess(tx):
    tx = tx.lower()
    stopw = readStopword()
    tx_list = [word for word in tx.split() if word not in stopw]
    return ' '.join(tx_list)

data_folder = "Data Kedua/TXTs"

X = []
Y = []

dirs = os.listdir(data_folder)
for d in dirs:
    for txt_file in os.listdir(os.path.join(data_folder, d)):
        with open(os.path.join(data_folder, d, txt_file),'r',encoding='utf-8') as tx:
            X.append(tx.read())
            Y.append(d)
            
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

count_vect = CountVectorizer(analyzer="word", ngram_range=(1,1))

train_data = count_vect.fit_transform(X_train)
test_data = count_vect.transform(X_test)

tfidf_transformer = TfidfTransformer()
train_data_tfidf = tfidf_transformer.fit_transform(train_data)
test_data_tfidf = tfidf_transformer.transform(test_data)

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

print("Multinomial NB - Bag of Words")
returnClassReport(clf1, train_data, y_train, test_data, y_test)

print("Multinomial NB - TF-IDF")
returnClassReport(clf1, train_data_tfidf, y_train, test_data_tfidf, y_test)

print("SVM - Bag of Words")
returnClassReport(clf2, train_data, y_train, test_data, y_test)

print("SVM - TF-IDF")
returnClassReport(clf2, train_data_tfidf, y_train, test_data_tfidf, y_test)
    
print("Random Forest - Bag of Words")
returnClassReport(clf3, train_data, y_train, test_data, y_test)

print("Random Forest - TF-IDF")
returnClassReport(clf3, train_data_tfidf, y_train, test_data_tfidf, y_test)

print("AdaBoost - Bag of Words")
returnClassReport(clf4, train_data, y_train, test_data, y_test)

print("AdaBoost - TF-IDF")
returnClassReport(clf4, train_data_tfidf, y_train, test_data_tfidf, y_test)

print("Decision Tree - Bag of Words")
returnClassReport(clf5, train_data, y_train, test_data, y_test)

print("Decision Tree - TF-IDF")
returnClassReport(clf5, train_data_tfidf, y_train, test_data_tfidf, y_test)

print("Decision Tree - Bag of Words")
returnClassReport(clf6, train_data, y_train, test_data, y_test)

print("Decision Tree - TF-IDF")
returnClassReport(clf6, train_data_tfidf, y_train, test_data_tfidf, y_test)
