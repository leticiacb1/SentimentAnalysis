import json
import boto3
import io

from config.config import Config

class LambdaFunction():
    def __init__(self):
        self.lambda_client  = None
        self.content_to_deploy = None

        self.layer_version  = None

        self.runtime = "python3.12"

        # Load environment variables
        self.config = Config()
        self.config.load()

    def create_client(self) -> None:
        self.lambda_client = boto3.client( "lambda",
                                            aws_access_key_id=self.config.ACCESS_KEY,
                                            aws_secret_access_key=self.config.SECRET_KEY,
                                            region_name=self.config.REGION
                                        )
        print("\n    [INFO] Create AWS lambda client. \n")

    def read_function(self, compress_filename: str) -> None:
        
        with open(compress_filename, "rb") as f:
            self.content_to_deploy = f.read()

        print("\n    [INFO] Read Content that will be deployed. \n")
        print(self.content_to_deploy)

    def create_function(self, function_handler: str, function_name: str) -> None:
        lambda_response = self.lambda_client.create_function( FunctionName=function_name,
                                                              Runtime=self.runtime,
                                                              Role=self.config.ROLE_ARN,
                                                              Handler=function_handler, 
                                                              Code={"ZipFile": self.content_to_deploy},
                                                            )

        print("\n    [INFO] Function ARN Response: \n")
        print("\n           > " + lambda_response["FunctionArn"])

    def publish_layer(self, layer_name: str, layer_package: str) -> None:
        print(f"\n    [INFO] Create a Layer Version with name {layer_name} and package {layer_package}. \n")

        with open(layer_package, "rb") as f:
            zip_to_deploy = f.read()

        lambda_response = self.lambda_client.publish_layer_version(
            LayerName=layer_name,
            Description="Layer with textblob for polarity",
            Content={"ZipFile": zip_to_deploy},
        )
        self.layer_version = lambda_response["LayerVersionArn"]

        print("\n           > Layer ARN:\n" + lambda_response["LayerArn"])
        print("\n           > Layer LayerVersionArn:\n" + lambda_response["LayerVersionArn"])

    def link_layer(self, function_name: str) -> None:
        
        print("\n    [INFO] Link Layer with the function. \n")
        
        response = self.lambda_client.get_function(FunctionName=function_name)
        print(response)

        layers = (
            response["Configuration"]["Layers"] if "Layers" in response["Configuration"] else []
        )

        print("\n    [INFO] Existing Layers: \n")
        print(layers)

        # Append the layer ARN to the existing layers
        if(self.layer_version == None):
            raise ValueError(" Layer_version not specified. Run function publish_layer first.")
        layers.append(self.layer_version)

        # Update the function configuration with the new layers
        lambda_response = self.lambda_client.update_function_configuration(
            FunctionName=function_name, Layers=layers
        )
        print("\n    [INFO] Lambda response: \n")
        print(lambda_response)

    def check_function(self, function_name: str, input: dict = None):

        try:
            if(not input):
                response = self.lambda_client.invoke( FunctionName=function_name,
                                                    InvocationType="RequestResponse",
                                                    )
            else:
                response = self.lambda_client.invoke( FunctionName=function_name,
                                                      InvocationType="RequestResponse",
                                                      Payload=json.dumps(input)
                                                    )
                                                
            payload = response["Payload"]

            txt = io.BytesIO(payload.read()).read().decode("utf-8")

            print(f"\n    [INFO] Invoke Function {function_name}(input = {input}) \n")
            print("\n           > Response :" + txt)

        except Exception as e:

            print(f"\n    [ERROR] Invoke Function {function_name}() \n")
            print(e)

    def see_all_lambda_functions(self):
        response = self.lambda_client.list_functions(MaxItems=1000)
        functions = response["Functions"]

        print(f"\n    [INFO] See all lambda functions associated to the account id \n")
        print(f"\n           > You have {len(functions)} Lambda functions")
        print(f"\n           > Functions names:")

        for function in functions:
            function_name = function["FunctionName"]
            print(f"           {function_name}")

    def _delete_function(self, function_name: str) -> None:

        if(self.lambda_client):
            self.lambda_client.delete_function(FunctionName=function_name)
            print(f"\n    [INFO] Lambda function {function_name} deleted successfully. \n")
        else:
            print(f"\n    [INFO] No Lambda function to delete. \n")

    def _delete_layer(self, layer_name: str) -> None:
        if(self.lambda_client):
            # Fetch the layer version ARN based on the layer name
            response = self.lambda_client.list_layer_versions(
                CompatibleRuntime= self.runtime,  # Provide the compatible runtime of the layer
                LayerName=layer_name,             # Must be the same runtime as lambda function
            )

            if "LayerVersions" in response:
                layer_versions = response["LayerVersions"]

                # Delete each layer version
                for version in layer_versions:
                    self.lambda_client.delete_layer_version(
                        LayerName=layer_name, VersionNumber=version["Version"]
                    )

                print(f"\n    [INFO] Deleted all versions of layer '{layer_name}'. \n")
            else:
                print(f"\n    [INFO] No layer with the name '{layer_name}' found. \n")
        else:
            print(f"\n    [INFO] No Layer to delete. \n")

    def cleanup(self, function_name: str, layer_name: str) -> None:

        # Delete the Lambda function
        self._delete_function(function_name = function_name)

        # Delete Layer
        self._delete_layer(layer_name = layer_name)