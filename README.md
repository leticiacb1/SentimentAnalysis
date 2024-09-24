### 🎭️ Sentiment Analysis (AWS Lambda Function)


The objective of this project is to **develop an API capable of analyzing the sentiment of a given sentence**. Using the `TextBlob library`, the API will process the received sentence and determine whether the expressed sentiment is positive, negative, or neutral. 

**Function as a Service (FaaS)** refers to a cloud computing model that allows developers to build and run applications and functions without having to worry about infrastructure management.

With FaaS, we are able to deploy their code in the form of stateless functions or event handlers that can be invoked on-demand or in response to events.

Every time there is a call to the API endpoint, whether through the browser or an application, the Lambda function will be triggered.

This will be the schematic drawing:

```bash
     ________            _____________           __________
    |        |          |             |         |          |
    |  API   |   <--->  | API Gateway |  <--->  |  Lambda  |
    |________|          |_____________|         |__________|
```

#### 📌 Run the project

**First Steps** 

Install **AWS CLI**, [click here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

```bash
# Configure credentials
$ aws configure --profile mlops
AWS Access Key ID [None]: ????????????
AWS Secret Access Key [None]: ????????????????????????????????
Default region name [None]: us-east-2
Default output format [None]:

# Set profile
$ export AWS_PROFILE=mlops

# List the names of lambda functions associated with your account:
$ aws lambda list-functions --query "Functions[*].FunctionName" --output text
```
<br>

Create a `venv` and install dependencies:

```bash
    # Create environment
    python3 -m venv venv  

    # Activate environment
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
``` 

Create a `.env` file inside `config/` folder :

```bash
    # .env content'
    AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
    AWS_SECRET_ACCESS_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaa"
    AWS_REGION="xx-xxxx-2"
    AWS_LAMBDA_ROLE_ARN="arn:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
``` 

For run a polarity example using `TextBlob`:

```bash
   python3 textblob_example.py
```

The file `polarity.py` contains the lmabda function that recive a sentence and return its polarity.
<br>

**How to get a Lambda Function with dependencies in Layers** 

First run your `docker desktop` then execute in the terminal:

```bash
# Create a container to install dependencies on
$ docker run -it ubuntu

# ------------------------------------
# --- Inside the container execute ---
# ------------------------------------

# Install python version:
$ apt update
$ apt install python3.12 python3-pip zip

# Create folder to install dependencies:
$ mkdir -p layer/python/lib/python3.12/site-packages
$ pip3 install textblob -t layer/python/lib/python3.12/site-packages

# Create a .zip with the dependencies:
$ cd layer
$ zip -r polarity_layer_package.zip *

# Check the results:
# Expected to see : polarity_layer_package.zip and python/ folder.
$ ls -la
# ----------End of container----------

# Extract zip from container:
$ docker ps -a  # Find container ID
$ docker cp <Container-ID:path_of_zip_on_container> <path_where_you_want_to_copy_the_zip>

# Example: docker cp ba7a7aba2b95:/layer/polarity_layer_package.zip ./
```

In the end of these commands you may have a `polarity_layer_package.zip` file in these project.

**Run the project** 

Run the project with the following command:

```bash
    python3 main.py
```

Code variables:

```python 
   # ---- Omitted Code ----

    lambda_filename = # Filename that contain the lambda function that will be deployed
    lambda_compress = # Name of filename that contain the zipped lambda function

    lambda_function_name =  # Lambda Function Name in AWS Lambda
    handler_function_name = # Funcion name that will be deplyed
    username = # Username of the account (Optional value)

    layer_name = # Function Layer name  
    layer_package = # .zip dependency package

    api_gateway_name = # Api name

    # ---- Omitted Code ----
``` 

**Attention** 

⚠️ It is possible that running the code more than once will report an error because the lambda function with that name has already been created. If this happens, change the code variable responsible for the function name (`lambda_function_name`) .

```bash
    # Error example:
    raise error_class(parsed_response, operation_name)
    botocore.errorfactory.ResourceConflictException: An error occurred (ResourceConflictException) 
    when calling the CreateFunction operation: Function already exist: say_hello3_leticiacb1
```

<br>
@2024, Insper. 9° Semester,  Computer Engineering.
<br>

_Machine Learning Ops & Interviews Discipline_
