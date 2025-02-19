import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

# ==================== Data Processing ================
# Load your dataset
data = pd.read_csv('Merged for ML.csv')

# Define numerical columns
num_cols = data.columns.drop('sum_duration_hrs')  # Exclude target column

# Define preprocessing for numerical features: impute missing values (if any) and scale
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),  # Fill missing values with mean
    ('scaler', StandardScaler())  # Standardize numerical values
])

# Since we have only numerical columns, we only use num_pipeline
preprocessor = ColumnTransformer([
    ('num', num_pipeline, num_cols)
])

# Apply the transformation
X = data.drop('sum_duration_hrs', axis=1)  # sum_duration_hrs is the outcome variable
y = data['sum_duration_hrs']  # Define target variable

# Create processed feature matrix
X_processed = preprocessor.fit_transform(X)

# Optional: Convert back to DataFrame for better readability
X_processed_df = pd.DataFrame(X_processed, columns=num_cols)

# Display processed data
print(X_processed_df.head())

# ============================= Baseline Model Development ====================
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.model_selection import train_test_split

# Split the processed data into training and testing sets (adjust test size as needed)
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.3, random_state=42)

# Initialize the LASSO regression model
# You may need to tune the alpha parameter (regularization strength) using cross-validation
baseline_model = Lasso(alpha=0.1, random_state=1)
baseline_model.fit(X_train, y_train)

# Predict on the test set
y_pred = baseline_model.predict(X_test)

# Evaluate performance using metrics such as Mean Absolute Error and Root Mean Squared Error
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("LASSO Regression Baseline Model")
print("Mean Absolute Error (MAE):", mae)
print("Root Mean Squared Error (RMSE):", rmse)


# ========================== Feature Importance and Interpretation ============
import numpy as np

# Assuming the model is linear (like LogisticRegression)
coefficients = baseline_model.coef_[0]
# If you want to map the coefficients back to feature names:
# First, get feature names from the preprocessor:
feature_names_num = num_cols
feature_names = np.concatenate([feature_names_num])
importance_df = pd.DataFrame({'feature': feature_names, 'coefficient': coefficients})
importance_df['abs_coef'] = importance_df['coefficient'].abs()
importance_df.sort_values(by='abs_coef', ascending=False, inplace=True)
print(importance_df.to_string())
