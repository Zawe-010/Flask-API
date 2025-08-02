import unittest 
from main import app
import json


class FlaskAPITest(unittest.TestCase):
    token = ""
    headers = {}
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"Flask-API Develop ":"1.0"})

    def test_login(self):
        response = self.app.post('/login', 
                                 data = json.dumps({"email":"maylynn@gmail.com", "password":"maylynn"}),
                                 content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        # Store token in global variable
        self.token = response.get_json()["token"]
        self.headers = {"Authorization" : "Bearer " + self.token, "Content-Type" : "application/json"}

    def test_products(self):
        # Call test_login() so that headers is given the token value        
        self.test_login()
        response = self.app.get('/api/products', headers = self.headers)
        self.assertEqual(response.status_code, 200)
        # print(response.get_json())

    def test_create_products(self):
        self.test_login()
        response = self.app.post("/api/products", data = json.dumps({"name" : "Chocolate", "buying_price" : 100, "selling_price" : 250}), 
                                 headers = self.headers, content_type = 'application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"name" : "Chocolate","buying_price" : 100, "selling_price" : 250})
    

    def test_sales(self):
        self.test_login()
        response = self.app.get('/api/sales', headers = self.headers)
        self.assertEqual(response.status_code, 200)
        # print(response.get_json())

    def test_create_sales(self):
        self.test_login()
        response = self.app.post("/api/sales", data = json.dumps({"pid" : 2, "quantity" : 10}),
                                 headers = self.headers, content_type ='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        # Validate only specific keys
        self.assertEqual(data["pid"], 2)
        self.assertEqual(data["quantity"], 10)

        # Confirm additional fields are present
        self.assertIn("id", data)
        self.assertIn("created_at", data)
        

if __name__ == "__main__":
    unittest.main()
