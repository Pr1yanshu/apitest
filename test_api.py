import unittest
import requests


class ApiTest(unittest.TestCase):
	pass


def testGen(endpoint, params, mode):
	if mode == "post":
		def check(self):
			req = requests.post(base_url + endpoint, params)
			self.assertEqual(req.status_code, 200)
		return check
	else:
		def check(self):
			target_url = base_url + endpoint
			encoded_data = "&".join([str(k) + "=" + str(v) for k, v in params.items()])
			req = requests.get(target_url + encoded_data)
			self.assertEqual(req.status_code, 200)
		return check


if __name__ == '__main__':
	base_url = "http://localhost:16000"
	args = [
		{"endpoint": "/post_location", "mode": "post", "data": {"lat": 70.23454, "lng": 80.1541651, "pin": 213421, "addr": "xyz", "cty": "Meerut"}},
		{"endpoint": "/get_location/", "mode": "get", "data": {"lat": 28.52424, "lng": 77.05505}},
		{"endpoint": "/get_using_postgre/", "mode": "get", "data": {"lat": 28.005523, "lng": 70.312412, "rad": 10000}},
		{"endpoint": "/get_using_self/", "mode": "get", "data": {"lat": 28.005523, "lng": 70.312412, "rad": 5000}}
	]
	for idx, arg in enumerate(args):
		test_id = "test_%d" % idx
		test = testGen(arg["endpoint"], arg["data"], arg["mode"])
		setattr(ApiTest, test_id, test)
	unittest.main()
