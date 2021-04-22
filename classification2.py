# adapted from https://www.datacamp.com/community/tutorials/decision-tree-classification-python
# and https://mljar.com/blog/visualize-decision-tree/
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn import tree
from matplotlib import pyplot as plt
'''

# *******************************************************
# method 1 to load iris dataset
from sklearn import datasets
# Prepare the data
iris = datasets.load_iris()
X = iris.data
y = iris.target
# Fit the classifier with default hyper-parameters
# *******************************************************
'''

# *******************************************************
# method 2 to load iris dataset
col_names = ['sl', 'sw', 'pl', 'pw', 'label']
# load dataset
data = pd.read_csv("iris.csv", header=None, names=col_names)

#split dataset in features and target variable
feature_cols = ['sl', 'sw', 'pl', 'pw']
X = data[feature_cols] # Features
y = data.label # Target variable
# Split dataset into training set 70% and test set 30%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) 

# Create Decision Tree classifer object
#clf = DecisionTreeClassifier()  # uses GINI value
#clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf = DecisionTreeClassifier(criterion="entropy")

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# visualize in text format
text_rep = tree.export_text(clf)
print(text_rep)
# to save to a file
with open("treeoutput.log", "w") as fout:
    fout.write(text_rep)

# visualize as decision tree plotted
fig = plt.figure(figsize=(25,20))
# *******************************************************

'''
# *******************************************************
# For Method 1
_ = tree.plot_tree(clf, 
                   feature_names=iris.feature_names,
                   class_names=iris.target_names,
                   filled=True)
# *******************************************************
'''

# *******************************************************
# For Method 2
_ = tree.plot_tree(clf, 
                   feature_names=feature_cols,  
                   class_names=['iris-s', 'iris-ve', 'iris-vi'],
                   filled=True)
# *******************************************************

# save tree image
fig.savefig("decision_tree.png")
plt.show()