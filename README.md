# Prediction API

tox compatible python versions

```
3.11
```

## Installation

### Setup virtual env

Make sure python3.11 is installed

```
$ python3.11 -m venv .venv
$ source .venv/bin/activate
```

### Installing Dependencies

```
$ pip install -U pip
$ pip install -r requirements.txt
```

## Local Development

Follow the steps below to run the tests faster.

```
$ pip install pytest-xdist
$ pytest -n auto
```

or directly tox:

```
$ tox
```

## Deployment

### Local deployment

```
$ python main.py api run-api
```

Then, API can be accessible at "http://localhost:5000":
1 - Openapi can be usable at "http://localhost:5000/docs" (apikey can be set as anything)
2 - cUrl can be usable with the command:

```
$ curl -X POST "http://localhost:5000/predict" -H "apikey: test" -H  "Content-Type: application/json" -d '{"Material_A_Charged_Amount": [[1.1]], "Material_B_Charged_Amount": [[1.2]], "Reactor_Volume": [[1.3]], "Material_A_Final_Concentration_Previous_Batch": [[1.4]]}'
```

### Running with docker

```
$ docker build -t app_image .
$ docker run -d --name app_container -p 80:80 app_image:latest
```

Then, API can be accessible at "http://localhost:80":
1 - Openapi can be usable at "http://localhost:80/docs" (apikey can be set as anything)
2 - cUrl can be usable with the command:

```
$ curl -X POST "http://localhost:80/predict" -H "apikey: test" -H  "Content-Type: application/json" -d '{"Material_A_Charged_Amount": [[1.1]], "Material_B_Charged_Amount": [[1.2]], "Reactor_Volume": [[1.3]], "Material_A_Final_Concentration_Previous_Batch": [[1.4]]}'
```

# Is ONNX an appropriate format to deploy the models? What are the benefits / drawbacks of using it?

While the ONNX has its challenges and limitations, it is widely used appropriate format to deploy the models.
The ONNX offers a potent remedy for the deep learning problems of model efficiency and interoperability.
Through the provision of a unified model representation format and an abundant tool and library ecosystem,
ONNX facilitates the smooth integration of various deep learning frameworks and platforms.
Its assistance with quantization and model optimization methods improves deep learning models' effectiveness even further.

## Benefits

### Interoperability of frameworks.

### Community assistance.

### Opportunities for optimization.

### Hardware-neutral.

### Regularity.

### Continual updates.

## Drawbacks

### Conversion's complexity.

### Compatibility between versions.

### Restricted assistance for specific tasks.

### In some cases, overheads in performance.

### The learning curve.

### Reliance on the community.

### Lack of support for dynamic neural networks.

### Periodic problems with compatibility.
