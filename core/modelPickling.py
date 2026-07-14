import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
import pickle

# Load the CSV file
try:
    data = pd.read_csv(r"C:\Users\FireShard\Documents\FYP\Data\laptopPrice_Cleaned.csv")
except FileNotFoundError:
    print("Error: CSV file not found. Please make sure the file exists in the correct directory.")
    exit()

# Handle missing values (if any)
data.fillna("Unknown", inplace=True)

# Select features and target
features = ['processor_brand', 'processor_name', 'processor_gnrtn', 'os_bit', 'brand', 'ram_gb']
target = 'ram_type'

X = data[features]
y = data[target]

# Convert categorical columns to lowercase
for col in X.select_dtypes(include=['object']).columns:
    X.loc[:, col] = X[col].str.lower()

# Encode categorical features and target
label_encoders = {}
for column in X.columns:
    if X[column].dtype == 'object':  # Encode only categorical columns
        label_encoders[column] = LabelEncoder()
        X.loc[:, column] = label_encoders[column].fit_transform(X[column])

label_encoders[target] = LabelEncoder()
y = label_encoders[target].fit_transform(y)

print(X,y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Decision Tree Classifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = metrics.accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the model and label encoders together
# Save the model
with open("laptop_ram_type_predictor_model.pkl", "wb") as f:
    pickle.dump(clf, f)

# Save the label encoders
with open("laptop_ram_type_predictor_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

print("Model and label encoders pickled successfully!")