import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# Load the dataset (needed to get feature names)
data = pd.read_csv('data/training_data.csv')
data = data.sample(frac=0.01, random_state=42) 

# Preprocess the data (to match the training data)
data['is_japanese_holiday'] = data['is_japanese_holiday'].astype(int)

# Define the features (excluding the target column)
X = data.drop(columns=['streaming'])

# Load the model from the file
model = joblib.load('data/model.pkl')

# Initialize SHAP explainer
explainer = shap.Explainer(model, X)

# Calculate SHAP values
shap_values = explainer(X)

# Plot the summary plot to show feature importance
shap.summary_plot(shap_values, X, plot_type="bar")

# Show the plot
plt.show()
