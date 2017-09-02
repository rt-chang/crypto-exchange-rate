import unittest
import json


from app import app


class TestApp(unittest.TestCase):

	def test_app(self):
		self.test_app = app.test_client()

		payload = {
			"result": {
				"source": "agent",
				"resolvedQuery": "CAD to USD",
				"action": "getExchangeRate",
				"parameters": {
					"currency-base": "CAD",
					"currency-target": "USD"
				}
			}
		}
		headers = {'content-type': 'application/json'}
		response = self.test_app.post('/webhook',
									  headers=headers,
									  data=json.dumps(payload))
		self.assertEqual(response.status, "200 OK")

if __name__ == '__main__':
	unittest.main()
