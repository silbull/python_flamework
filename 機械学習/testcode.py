import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Load datasets
iris = datasets.load_iris()

# Load as pandas.DataFrame
df_iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Add target
df_iris['target'] = iris.target

print(df_iris)

# Split the dataset
data_train, data_test, target_train, target_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=0)

# Define Neural Neowork model
clf = MLPClassifier(hidden_layer_sizes=10, activation='relu',
                    solver='adam', max_iter=1000)

# Lerning model
clf.fit(data_train, target_train)

# Calculate prediction accuracy
print(clf.score(data_train, target_train))

# Predict test data
print(clf.predict(data_test))

# Show loss curve
plt.plot(clf.loss_curve_)
plt.title("Loss Curve")
plt.xlabel("Iteration")
plt.ylabel("Loss")
plt.grid()
plt.show()