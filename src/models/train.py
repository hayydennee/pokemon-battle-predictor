# Importing necessary libraries
import pandas as pd

# Using pandas, splitting the dataset into features (X) and target variable (y)
df = pd.read_csv('data/processed/features.csv')

# Dropping the 'label' column from the dataset to create the features (X) and assigning the 'label' column to the target variable (y)
x = df.drop(columns=['label'])
y = df['label']

# Splitting input data into training and validation sets
from sklearn.model_selection import train_test_split

# test_size=0.2 means that 20% of the data will be used for testing and 80% for training. random_state=42 ensures that the split is reproducible.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Using XGBoost to create model object and fit the model to the training data
from xgboost import XGBClassifier

model = XGBClassifier()

# Training the model using the fit method, which takes the training features (x_train) and training labels (y_train) as input.
model.fit(x_train, y_train)

# Classification report to evaluate the performance of the model on the test set
from sklearn.metrics import classification_report

y_pred = model.predict(x_test)

# Precision is the ratio of true positive predictions to the total predicted positives
# Recall is the ratio of true positive predictions to the total actual positives
# F1-score is the harmonic mean of precision and recall. 
# Support is the number of actual occurrences of the class in the test set.
# The classification report will show these metrics for each class in the target variable.
print(classification_report(y_test, y_pred))

# Save trained model to src/models/model.json
model.save_model('src/models/model.json')