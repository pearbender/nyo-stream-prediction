import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load the dataset
data = pd.read_csv('data/training_data.csv')

# Check for duplicate rows in the dataset
duplicates = data.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

# Preprocess the data
# Convert boolean columns to integers
data['is_japanese_holiday'] = data['is_japanese_holiday'].astype(int)
data['streaming'] = data['streaming'].astype(int)

# Define the features and target
X = data.drop(columns=['streaming'])
y = data['streaming']

true_false_counts = y.value_counts()
print('Count of True and False values in target variable:')
print(true_false_counts)

# Split the data into training and testing sets with a stratified split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize the Gradient Boosting Classifier with reduced complexity
model = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42, verbose=1)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Generate and print the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:')
print(conf_matrix)

# Save the model
joblib.dump(model, 'data/model.pkl')
