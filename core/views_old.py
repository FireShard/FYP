from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from sklearn.preprocessing import OneHotEncoder

import joblib
import os
import pickle
import pandas as pd
import json

# Load the pickled model and label encoders
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptop_model.pkl')

# with open(model_path, "rb") as f:
#     loaded_data = pickle.load(f)
#     model = loaded_data['model']
#     label_encoders = loaded_data['label_encoders']

model = joblib.load(model_path)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
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

            processor_brand = data.get('processor_brand', None),
            processor_name = data.get('processor_name', None),
            processor_gnrtn = data.get('processor_gnrtn', None),
            os_bit = data.get('os_bit', None),
            brand = data.get('brand', None),
            ram_gb = data.get('ram_gb', None),
            ram_type = "",

            frontdata = []
            frontdata.append([
                processor_brand,
                processor_name,
                processor_gnrtn,
                os_bit,
                brand,
                ram_gb,
            ])

            frontdata_df = pd.DataFrame(frontdata)

            # if not isinstance(data, list): 
            #     data = [data]  # Convert to a list if it's a single dictionary
            df = pd.DataFrame(frontdata_df)

            # Convert categorical columns to lowercase
            for col in df.select_dtypes(include=['object']).columns:
                df.loc[:, col] = df[col].str.lower()

            # # One-hot encode categorical features
            # categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
            # encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            # encoder.fit(df[categorical_cols])
            # X_encoded = pd.DataFrame(encoder.transform(df[categorical_cols]))
            # encoded_col_names = encoder.get_feature_names_out(categorical_cols)
            # X_encoded.columns = encoded_col_names.astype(str)
            # df = pd.concat([df.drop(categorical_cols, axis=1), X_encoded], axis=1)            

            # Make prediction
            prediction = model.predict(df)[0]
            print(prediction)

            # return JsonResponse({'prediction': prediction})
            return JsonResponse(prediction, safe=False)
        
        except Exception as e:
            if isinstance(e, KeyError):
                return JsonResponse({'error': 'Missing required field in data','errmessage':e}, status=400)
            elif isinstance(e, pickle.UnpicklingError):
                return JsonResponse({'error': 'Error unpickling model or encoders. Please check file integrity.','errmessage':e}, status=500)
            elif isinstance(e, ValueError):
                return JsonResponse({'error': 'Invalid data format. Please check data types.','errmessage':e}, status=400)
            else:
                return JsonResponse({'error': str(e)}, status=500)

model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptop_ram_type_predictor.pkl')

with open(model_path, "rb") as f:
     loaded_data = pickle.load(f)
     model = loaded_data['model']
     label_encoders = loaded_data['label_encoders']

model = joblib.load(model_path)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
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

            processor_brand = data.get('processor_brand', None).lower(),
            processor_name = data.get('processor_name', None).lower(),
            processor_gnrtn = data.get('processor_gnrtn', None),
            os_bit = data.get('os_bit', None),
            brand = data.get('brand', None).lower(),
            ram_gb = data.get('ram_gb', None),
            

            input_data = pd.DataFrame({
                'processor_brand': processor_brand,
                'processor_name': processor_name,
                'processor_gnrtn': processor_gnrtn,
                'os_bit': os_bit,
                'brand': brand,
                'ram_gb': ram_gb
            })

            print("Input data:", input_data)

            for column in input_data.columns:
                if column in label_encoders:
                    input_data.loc[:, column] = label_encoders[column].transform(input_data[column])        

            # Make prediction
            prediction = model.predict(input_data)[0]
            predicted_ram_type = label_encoders['ram_type'].inverse_transform(prediction)[0]
            return JsonResponse(prediction, safe=False)
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

model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'ram_type_predictor.pkl')

with open(model_path, "rb") as f:
     model = pickle.load(f)

model = joblib.load(model_path)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
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

            processor_brand = data.get('processor_brand', None).lower(),
            processor_name = data.get('processor_name', None).lower(),
            processor_gnrtn = data.get('processor_gnrtn', None),
            os_bit = data.get('os_bit', None),
            brand = data.get('brand', None).lower(),
            ram_gb = data.get('ram_gb', None),
            

            input_data = pd.DataFrame({
                'processor_brand': processor_brand,
                'processor_name': processor_name,
                'processor_gnrtn': processor_gnrtn,
                'os_bit': os_bit,
                'brand': brand,
                'ram_gb': ram_gb
            })

            print("Input data:", input_data)
  

            # Make prediction
            predicted_ram_type = model.predict(input_data)
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

model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptop_ram_type_predictor.pkl')
encoder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptop_ram_type_predictor.pkl')

with open(model_path, "rb") as f:
     model = pickle.load(f)

with open(encoder_path, "rb") as f:
     label_encoders = pickle.load(f)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    def post(self, request, *args, **kwargs):
        try:
            #Exception Handling
            required_fields = ['processor_brand', 'ram_gb', 'os_bit', 'brand', 'processor_name', 'processor_gnrtn']
            # print("Received data:", json.loads(request.body))
            fields_recieve = list(json.loads(request.body).keys())
            print(type(model))
            print("fields_recieve data:", fields_recieve)
            for field in required_fields:
                if field not in fields_recieve:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

            data = json.loads(request.body)

            processor_brand = data.get('processor_brand', None).lower()
            processor_name = data.get('processor_name', None).lower()
            processor_gnrtn = data.get('processor_gnrtn', None)
            os_bit = data.get('os_bit', None)
            brand = data.get('brand', None).lower()
            ram_gb = data.get('ram_gb', None)
            

            input_data = pd.DataFrame({
                'processor_brand': [processor_brand],
                'processor_name': [processor_name],
                'processor_gnrtn': [processor_gnrtn],
                'os_bit': [os_bit],
                'brand': [brand],
                'ram_gb': [ram_gb]
            })

            print("Input data:", input_data)

            for column in input_data.columns:
                if column in label_encoders:
                    input_data.loc[:, column] = label_encoders[column].transform(input_data[column])        

            # Make prediction
            prediction = model.predict(input_data)[0]
            predicted_ram_type = label_encoders['ram_type'].inverse_transform(prediction)[0]
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