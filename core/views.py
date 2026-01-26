from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

import joblib
import os
import pickle
import json
import re

import pandas as pd
from nltk.metrics import edit_distance 
from jellyfish import jaro_winkler_similarity 
from fuzzywuzzy import fuzz  

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

trainData = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptopPrice_Cleaned.csv')

@method_decorator(csrf_exempt, name='dispatch')
class PredictRAMTypeView(View):
    def post(self, request, *args, **kwargs):
        try:
            #Exception Handling
            required_fields = ['processor_brand', 'ram_gb', 'os_bit', 'brand', 'processor_name', 'processor_gnrtn']
            # print("Received data:", json.loads(request.body))
            fields_recieve = list(json.loads(request.body).keys())
            print("fields_recieve data:", fields_recieve)
            for field in required_fields:
                if field not in fields_recieve:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

            data = json.loads(request.body)

            processor_brand = data.get('processor_brand', None).lower()
            processor_name = data.get('processor_name', None).lower()
            processor_gnrtn = data.get('processor_gnrtn', None).lower()
            os_bit = data.get('os_bit', None)
            brand = data.get('brand', None).lower()
            ram_gb = data.get('ram_gb', None)
            

            try:
                data = pd.read_csv(trainData)
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

            # Calculate class weights dynamically (using pandas Series)
            y_series = pd.Series(y)  # Convert y to pandas Series
            class_counts = y_series.value_counts() 
            class_weights = {label: 1.0 / count for label, count in class_counts.items()}

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train the Decision Tree Classifier with class weights
            clf = DecisionTreeClassifier(class_weight=class_weights)
            clf.fit(X_train, y_train)

            input_data = pd.DataFrame({
                'processor_brand': [processor_brand],
                'processor_name': [processor_name],
                'processor_gnrtn': [processor_gnrtn],
                'os_bit': [os_bit],
                'brand': [brand],
                'ram_gb': [ram_gb],
            })

            print("Input data:", input_data)

            for column in input_data.columns:
                if column in label_encoders:
                    input_data.loc[:, column] = label_encoders[column].transform(input_data[column])

            prediction = clf.predict(input_data)
            predicted_ram_type = label_encoders[target].inverse_transform(prediction)[0]
            return JsonResponse(predicted_ram_type, safe=False)
        except ValueError as e:
            print(f"Error during prediction: {e}. The input value might not be in the training data.")
            return None
        
        except Exception as e:
            if isinstance(e, KeyError):
                return JsonResponse({'error': 'Missing required field in data','errmessage':e}, status=400)
            elif isinstance(e, pickle.UnpicklingError):
                return JsonResponse({'error': 'Error unpickling model or encoders. Please check file integrity.','errmessage':e}, status=500)
            elif isinstance(e, ValueError):
                return JsonResponse({'error': 'Invalid data format. Please check data types.','errmessage':e}, status=400)
            else:
                return JsonResponse({'error': str(e)}, status=500)


trainDataComp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'combined_ram_types.csv')

@method_decorator(csrf_exempt, name='dispatch')
class PredictCompatibilityView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            parsed_word1 = data.get('word1', None)
            parsed_word2 = data.get('word2', None)

            print("Received data:", json.loads(request.body))

            # Load data from CSV
            data = pd.read_csv(trainDataComp) 

            # Feature engineering
            data['levenshtein_distance'] = data.apply(lambda row: edit_distance(row['ram_type_df1'], row['ram_type_df2']), axis=1)
            data['jaro_winkler_distance'] = data.apply(lambda row: jaro_winkler_similarity(row['ram_type_df1'], row['ram_type_df2']), axis=1)
            data['partial_ratio'] = data.apply(lambda row: fuzz.partial_ratio(row['ram_type_df1'], row['ram_type_df2']), axis=1)
            data['token_sort_ratio'] = data.apply(lambda row: fuzz.token_sort_ratio(row['ram_type_df1'], row['ram_type_df2']), axis=1)

            # Select features
            features = ['levenshtein_distance', 'jaro_winkler_distance', 'partial_ratio', 'token_sort_ratio']
            X = data[features]
            y = data['is_similar']

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train logistic regression model
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)

            # Make predictions
            y_pred = model.predict(X_test)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
        # Make prediction based on the input
        def predict_word_similarity(word1, word2):
            """
            Predicts whether two words are similar based on the trained logistic regression model.

            Args:
                word1: The first word.
                word2: The second word.

            Returns:
                A string indicating whether the words are predicted to be 'same' or 'different'.
            """

            # Feature engineering for the input words
            features = [
                edit_distance(word1, word2),
                jaro_winkler_similarity(word1, word2),
                fuzz.partial_ratio(word1, word2),
                fuzz.token_sort_ratio(word1, word2)
            ]

            # Create a DataFrame for the input features with the correct column names
            input_df = pd.DataFrame([features], columns=X.columns) 

            # Make prediction
            prediction = model.predict(input_df)

            if prediction[0] == 1:
                return 'same'
            else:
                return 'different'

        # Extract ram type form url
        def extract_ram_types_from_url(url):
            """
            Extracts potential RAM types from a given URL.

            Args:
                url: The URL to extract RAM types from.

            Returns:
                A list of potential RAM types found in the URL.
            """
            possible_ram_types = ['DDR1','DDR2','DDR3', 'DDR4', 'DDR5', 'LPDDR3', 'LPDDR4', 'LPDDR4X']
            ram_types_found = []

            for ram_type in possible_ram_types:
                if ram_type in url:
                    ram_types_found.append(ram_type)

            return ram_types_found
        
        # Check for blacklisted word
        def check_for_blacklist_words(url):
            """
            Checks if the URL contains any of the blacklisted words, treating hyphens as word boundaries.
            Allows the URL if a whitelisted word is also present.

            Args:
                url: The URL to check.

            Returns:
                False if the URL is allowed (contains a whitelisted word or no blacklisted words), 
                True otherwise.
            """
            blacklisted_words = ['Desktop', 'DIMM', 'PC']
            whitelisted_words = ['Laptop', 'SODIMM', 'Notebook']

            # Create regular expression patterns
            blacklist_pattern = r"\b(" + "|".join(blacklisted_words) + r")\b"
            whitelist_pattern = r"\b(" + "|".join(whitelisted_words) + r")\b"

            # Check for blacklisted words
            if re.search(blacklist_pattern, url, re.IGNORECASE):
                # If a blacklisted word is found, check for a whitelisted word
                if re.search(whitelist_pattern, url, re.IGNORECASE):
                    return False  # Allow if a whitelisted word is present
                else:
                    return True  # Block if no whitelisted word is found

            # No blacklisted words found, allow the URL
            return False
        
        # Main def for analyzing the inputed url
        def analyze_url(url, word1):
            """
            Analyzes the given URL for compatibility.

            Args:
                url: The URL to analyze.
                word1: The input RAM type.

            Returns:
                A string indicating the compatibility:
                    - "Compatible" if the URL is compatible with the specified RAM types.
                    - "Incompatible" if the URL is not compatible.
                    - "Error" if an error occurred during analysis.
            """
            try:
                ram_types_in_url = extract_ram_types_from_url(url)

                if not ram_types_in_url:
                    return "Incompatible: The Shopee listing not selling a DDR RAM type."

                if check_for_blacklist_words(url):
                    return "Incompatible: The RAM in the Shopee listing is not for laptops." 

                # If word1 is an LPDDR type and any LPDDR type is found in the URL, reject
                if "LPDDR" in word1 and any(lpdrr_type in url for lpdrr_type in ['LPDDR3', 'LPDDR4', 'LPDDR4X']):
                    return "Incompatible: Your laptop uses a LPPDR RAM type."

                # Check each RAM type in the URL
                for ram_type in ram_types_in_url:
                    if predict_word_similarity(word1, ram_type) == 'same':
                        return "Compatible: The RAM in the Shopee listing is compatible with your laptop's RAM type"

                return "Incompatible: The RAM in the Shopee listing is incompatible with your laptop's RAM type."
            
            except Exception as e:
                return f"Error: {str(e)}"

        # Get input
        word1 = parsed_word1
        url = parsed_word2

        # Analyze the URL
        result = analyze_url(url, word1)

        # Print the result
        print(f"URL Analysis: {result}")
        return JsonResponse(result, safe=False)        

        


