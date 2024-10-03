import unittest

from parameterized import parameterized
from fastapi.testclient import TestClient
from fastapi import status

from api.app import app

class TestRegressionAPI(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app, raise_server_exceptions=False, headers={"apikey": "test"})

    def get_api_path(self) -> str:
        return self.client.app.url_path_for("prediction_api")

    @parameterized.expand([
        (
            {},
            {
                "detail":[
                    {
                        "type": "value_error",
                        "loc": ["body"],
                        "msg": "Value error, The data for all inputs should be provided correctly.",
                        "input": {},
                        "ctx": {"error": {}}
                    }
                ]
            }
        ),
        (
            {"Material_A_Charged_Amount": []},
            {
                "detail":[
                    {
                        "type": "too_short",
                        "loc": ["body", "Material_A_Charged_Amount"],
                        "msg": "List should have at least 1 item after validation, not 0",
                        "input": [],
                        "ctx": {"field_type": "List", "min_length": 1, "actual_length": 0}
                    }
                ]
            }
        ),
        (
            {"Material_A_Charged_Amount": [[]]},
            {
                "detail":[
                    {
                        "type": "too_short",
                        "loc": ["body", "Material_A_Charged_Amount", 0],
                        "msg": "List should have at least 1 item after validation, not 0",
                        "input": [],
                        "ctx": {"field_type": "List", "min_length": 1, "actual_length": 0}
                    }
                ]
            }
        ),
        (
            {"Material_A_Charged_Amount": [[1.1]]},
            {
                'detail': [
                    {
                        'type': 'value_error',
                        'loc': ['body'],
                        'msg': 'Value error, The data for all inputs should be provided correctly.',
                        'input': {'Material_A_Charged_Amount': [[1.1]]},
                        'ctx': {'error': {}},
                    }
                ]
            }
        ),
        (
            {
                "Material_A_Charged_Amount": [[1.5], [22]],
                "Material_B_Charged_Amount": [[2.3]],
                "Reactor_Volume": [[4.5]],
                "Material_A_Final_Concentration_Previous_Batch": [[1.2]],
            },
            {
                'detail': [
                    {
                        'type': 'value_error',
                        'loc': ['body'],
                        'msg': 'Value error, All values must have same number of items.',
                        'input': {
                            'Material_A_Charged_Amount': [[1.5], [22]],
                            "Material_B_Charged_Amount": [[2.3]],
                            "Reactor_Volume": [[4.5]],
                            "Material_A_Final_Concentration_Previous_Batch": [[1.2]],
                        },
                        'ctx': {'error': {}},
                    }
                ]
            }
        ),
    ])
    def test__invalid_request(self, invalid_request, expected_error):
        response = self.client.post(
            url=self.get_api_path(),
            json=invalid_request
        )
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code, msg=response.content)
        self.assertEqual(
            expected_error,
            response.json()
        )

    def test__min_response(self):
        request_data = {
            "Material_A_Charged_Amount": [[1.5]],
            "Material_B_Charged_Amount": [[2.3]],
            "Reactor_Volume": [[4.5]],
            "Material_A_Final_Concentration_Previous_Batch": [[1.2]],
        }
        response = self.client.post(
            url=self.get_api_path(),
            json=request_data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        self.assertEqual(
            [
                {
                    'output_label': 'High',
                    'output_probability': {
                        'Good': 0.2577363848686218,
                        'High': 0.6922637224197388,
                        'Low': 0.05000000074505806
                    }
                }
            ],
            response.json()
        )

    def test__max_response(self):
        request_data = {
            "Material_A_Charged_Amount": [[1.5], [5.7]],
            "Material_B_Charged_Amount": [[2.3], [2.1]],
            "Reactor_Volume": [[4.5], [3.2]],
            "Material_A_Final_Concentration_Previous_Batch": [[1.2], [99.999]],
        }
        response = self.client.post(
            url=self.get_api_path(),
            json=request_data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        self.assertEqual(
            [
                {
                    'output_label': 'High',
                    'output_probability': {
                        'Good': 0.2577363848686218,
                        'High': 0.6922637224197388,
                        'Low': 0.05000000074505806
                    }
                },
                {
                    'output_label': 'High',
                    'output_probability': {
                        'Good': 0.1744595319032669,
                        'High': 0.8152548670768738,
                        'Low': 0.010285714641213417
                    }
                }
            ],
            response.json()
        )
