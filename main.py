from dataclass.compress import CompressFile
from dataclass.lambda_function import LambdaFunction
from dataclass.gateway import Gateway

import time
import requests

# Variaveis
lambda_filename = "polarity.py"
lambda_compress = "polarity.zip"

lambda_function_name = "get_polarity"   # Change Function Name in AWS Lambda
handler_function_name = "get_polarity"  # Funcion name in file hello.py
username = "leticiacb1"         

layer_name = "layer_polarity_" + username    
layer_package = "polarity_layer_package.zip" # Dependency package

input_json = {
    "sentence": "This was the worst movie I watched this year, horrible!"
}

api_gateway_name = "api_sentimentAnalysis_leticiacb1"


handler = lambda_filename.split('.')[0] + "." + handler_function_name
function_name = lambda_function_name + "_" + username 

try: 
    # Instances
    compress = CompressFile()
    _lambda = LambdaFunction()
    gateway = Gateway()

    # Compress
    compress.run(lambda_filename=lambda_filename, compress_filename=lambda_compress)

    # Lambda Function
    _lambda.create_client()
    _lambda.read_function(compress_filename=lambda_compress)
    _lambda.create_function(function_handler= handler, function_name=function_name)
    _lambda.publish_layer(layer_name=layer_name, layer_package=layer_package)
    _lambda.link_layer(function_name=function_name)

    time.sleep(1) # Wait lambda function to be deployed

    _lambda.check_function(function_name=function_name)
    _lambda.see_all_lambda_functions()

    # Create API for access lambda function
    gateway.create_client()
    gateway.get_lambda_function(function_name=function_name)
    gateway.create_api(api_name= api_gateway_name)
    gateway.set_permissions(function_name=function_name)
    gateway.create_route(HTTP_method="POST", route_key="POST /polarity")
    gateway.see_all_gateways()

    # Test the API response
    print(f"\n    [INFO] Test API.\n")
    api_response = requests.post(gateway.endpoint, json=input_json)
    print(api_response.json())

except Exception as e:
    print(f"\n    [ERROR] An error occurred: \n {e}")
finally:
    # Cleaning:
    gateway.cleanup(api_name= api_gateway_name)
    _lambda.cleanup(function_name=function_name, layer_name=layer_name)