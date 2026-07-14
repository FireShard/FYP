from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

import os
import pickle
import pandas as pd
import json

# Load the pickled model and label encoders
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptop_ram_type_predictor.pkl')

with open(model_path, "rb") as f:
    loaded_data = pickle.load(f)
    model = loaded_data['model']
    label_encoders = loaded_data['label_encoders']

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    def post(self, request, *args, **kwargs):
        try:
            required_fields = ['processor_brand', 'ram_gb', 'os_bit', 'brand', 'processor_name', 'processor_gnrtn']
            for field in required_fields:
                if field not in request.POST:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

            # Get data from the request body
            data = json.loads(request.body)

            ordered_data = {
                'processor_brand': data.get('processor_brand', None),
                'processor_name': data.get('processor_name', None),
                'processor_gnrtn': data.get('processor_gnrtn', None),
                'os_bit': data.get('os_bit', None),
                'brand': data.get('brand', None),
                'ram_gb': data.get('ram_gb', None)
            }

            # Convert categorical features to lowercase (same as in the model)
            for col in ordered_data.keys():
                if col in label_encoders:
                    data[col] = data[col].lower()

            # Encode the data using the loaded label encoders
            encoded_data = {}
            for col, enc in label_encoders.items():
                encoded_data[col] = enc.transform([ordered_data[col]])[0]

            # Create a DataFrame from the encoded data
            input_data = pd.DataFrame(encoded_data)

            # Make prediction using the loaded model
            prediction = model.predict(input_data)
            predicted_ram_type = label_encoders['ram_type'].inverse_transform(prediction)[0]

            return JsonResponse({'predicted_ram_type': predicted_ram_type})
        except Exception as e:
            if isinstance(e, KeyError):
                return JsonResponse({'error': 'Missing required field in data'}, status=400)
            elif isinstance(e, pickle.UnpicklingError):
                return JsonResponse({'error': 'Error unpickling model or encoders. Please check file integrity.'}, status=500)
            elif isinstance(e, ValueError):
                return JsonResponse({'error': 'Invalid data format. Please check data types.'}, status=400)
            else:
                return JsonResponse({'error': str(e)}, status=500)

async predictRamType() {
                try {
                    const predictRamType = {
                        processor_brand: this.CPUbrand,
                        processor_name: this.CPUName,
                        processor_gnrtn: this.CPUGen,
                        os_bit: this.architecture,
                        brand: this.manufacturer,
                        ram_gb: this.ramSize,
                    };
                    const response = await axios
                        .post("http://127.0.0.1:8000/predict/", predictRamType)
                        // .then(response => {
                        //     console.log("RAM Type Predicted Successfully", response.data);
                        //     alert("RAM Type Predicted Successfully!");
                        //     // this.goToRecommend();
                        // })
                        // .catch((error) =>{
                        //     console.error("Error in predicting RAM type", error);
                        //     alert("Failed in predicting RAM type. Please try again");
                        // });
                        console.log("RAM Type Predicted Successfully", response.data);
                        alert("RAM Type Predicted Successfully!");

                        this.ramType = response.data.predicted_ram_type;
                } 
                catch (error) {
                    console.error('Error predicting RAM type:', error);
                    this.ramType = 'Prediction Failed';
                    alert("Failed in predicting RAM type. Please try again");
                }

                // const newUserLaptop = {
                //     manufacturer: this.manufacturer,
                //     ramSize: this.ramSize,
                //     architecture: this.architecture,
                //     CPUbrand: this.CPUbrand,
                //     CPUName: this.CPUName,
                //     CPUGen: this.CPUGen,
                //     ramType: this.ramType,
                //     ramid: this.ramid
                // };

                // axios
                //     .post("http://127.0.0.1:8000/UserLaptop/", newUserLaptop)
                //     .then(response => {
                //         console.log("Added Laptop Details Successfully", response.data);
                //         alert("Added Laptop Details Successfully!");
                //         this.goToRecommend();
                //     })
                //     .catch((error) =>{
                //         console.error("Error in saving laptop data", error);
                //         alert("Failed in saving laptop data. Please try again");
                //     }) 

            },

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
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'primaryApp', 'laptop_ram_type_predictor.pkl')

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

            # Get data from the request body
            # data = json.loads(request.body)
            # print("Received data:", data)

            data = json.loads(request.body) 
            if not isinstance(data, list): 
                data = [data]  # Convert to a list if it's a single dictionary
            df = pd.DataFrame(data) 

            df = pd.DataFrame({
                'processor_brand': data.get('processor_brand', None).lower(),
                'processor_name': data.get('processor_name', None).lower(),
                'processor_gnrtn': data.get('processor_gnrtn', None).lower(),
                'os_bit': data.get('os_bit', None),
                'brand': data.get('brand', None).lower(),
                'ram_gb': data.get('ram_gb', None)
            })

            # One-hot encode categorical features
            categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            encoder.fit(df[categorical_cols])
            X_encoded = pd.DataFrame(encoder.transform(df[categorical_cols]))
            encoded_col_names = encoder.get_feature_names_out(categorical_cols)
            X_encoded.columns = encoded_col_names.astype(str)
            df = pd.concat([df.drop(categorical_cols, axis=1), X_encoded], axis=1)            

            # ordered_data = data

            # Convert categorical features to lowercase (same as in the model)
            # print(data.keys())
            # for col in list(data.keys()):
            #     if col in label_encoders:
            #         data[col] = data[col].lower()

            # Encode the data using the loaded label encoders
            # encoded_data = {}
            # for col, enc in label_encoders.items():
            #     encoded_data[col] = enc.transform([ordered_data[col]])[0]

            # Create a DataFrame from the encoded data
            # input_data = pd.DataFrame(encoded_data)

            # Make prediction using the loaded model
            # prediction = model.predict(input_data)
            # predicted_ram_type = label_encoders['ram_type'].inverse_transform(prediction)[0]

            # Make prediction
            prediction = model.predict(data)[0]

            # Get the predicted RAM type
            # predicted_ram_type = target.iloc[np.where(y == prediction)[0][0]]

            # return JsonResponse({'predicted_ram_type': predicted_ram_type})
            return JsonResponse({'prediction': prediction})
        
        except Exception as e:
            if isinstance(e, KeyError):
                return JsonResponse({'error': 'Missing required field in data','errmessage':e}, status=400)
            elif isinstance(e, pickle.UnpicklingError):
                return JsonResponse({'error': 'Error unpickling model or encoders. Please check file integrity.','errmessage':e}, status=500)
            elif isinstance(e, ValueError):
                return JsonResponse({'error': 'Invalid data format. Please check data types.','errmessage':e}, status=400)
            else:
                return JsonResponse({'error': str(e)}, status=500)
            

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

            # Get data from the request body
            # data = json.loads(request.body)
            # print("Received data:", data)

            data = json.loads(request.body) 
            if not isinstance(data, list): 
                data = [data]  # Convert to a list if it's a single dictionary
            df = pd.DataFrame(data) 

            df = pd.DataFrame({
                'processor_brand': data.get('processor_brand', None).lower(),
                'processor_name': data.get('processor_name', None).lower(),
                'processor_gnrtn': data.get('processor_gnrtn', None).lower(),
                'os_bit': data.get('os_bit', None),
                'brand': data.get('brand', None).lower(),
                'ram_gb': data.get('ram_gb', None)
            })

            # One-hot encode categorical features
            categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            encoder.fit(df[categorical_cols])
            X_encoded = pd.DataFrame(encoder.transform(df[categorical_cols]))
            encoded_col_names = encoder.get_feature_names_out(categorical_cols)
            X_encoded.columns = encoded_col_names.astype(str)
            df = pd.concat([df.drop(categorical_cols, axis=1), X_encoded], axis=1)            

            # ordered_data = data

            # Convert categorical features to lowercase (same as in the model)
            # print(data.keys())
            # for col in list(data.keys()):
            #     if col in label_encoders:
            #         data[col] = data[col].lower()

            # Encode the data using the loaded label encoders
            # encoded_data = {}
            # for col, enc in label_encoders.items():
            #     encoded_data[col] = enc.transform([ordered_data[col]])[0]

            # Create a DataFrame from the encoded data
            # input_data = pd.DataFrame(encoded_data)

            # Make prediction using the loaded model
            # prediction = model.predict(input_data)
            # predicted_ram_type = label_encoders['ram_type'].inverse_transform(prediction)[0]

            # Make prediction
            prediction = model.predict(data)[0]

            # Get the predicted RAM type
            # predicted_ram_type = target.iloc[np.where(y == prediction)[0][0]]

            # return JsonResponse({'predicted_ram_type': predicted_ram_type})
            return JsonResponse({'prediction': prediction})
        
        except Exception as e:
            if isinstance(e, KeyError):
                return JsonResponse({'error': 'Missing required field in data','errmessage':e}, status=400)
            elif isinstance(e, pickle.UnpicklingError):
                return JsonResponse({'error': 'Error unpickling model or encoders. Please check file integrity.','errmessage':e}, status=500)
            elif isinstance(e, ValueError):
                return JsonResponse({'error': 'Invalid data format. Please check data types.','errmessage':e}, status=400)
            else:
                return JsonResponse({'error': str(e)}, status=500)