from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load dataset
df = pd.read_excel(r'E:\Learning\undergraduate\2021 Fall\CS397\data_labeling.xlsx', sheet_name='dataset')
x = df.iloc[:, [0, 6]].values
y = df.iloc[:, 7].values

# Split our data
# Test set = 30% original dataset
train, test, train_labels, test_labels = train_test_split(x, y, test_size=0.3, random_state=5)

# Feature Scaling
sc = StandardScaler()
train = sc.fit_transform(train)
test = sc.transform(test)

# Initialize our classifier
gnb = GaussianNB()

# Train our classifier
model = gnb.fit(train, train_labels)

# Make predictions
preds = gnb.predict(test)
print(preds)

# Evaluate accuracy
print('Accuracy = ',accuracy_score(test_labels, preds))