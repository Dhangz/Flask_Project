import unittest
from api import app  # Assuming your Flask app is in a file named api.py
import warnings

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Python Flask CRUD Application", response.data)

    def test_insert(self):
        response = self.app.post("/insert", data=dict(
            born_in_litter_id=1,
            dog_name="browny",
            gender_mf="M",
            date_of_birth="2023-01-01",
            place_of_birth="puerto princesa city",
            other_details="friendly"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data Inserted Successfully", response.data)

    def test_update(self):
        response = self.app.post("/update/5", data=dict(
            dog_id=5,
            dog_name="blacky",
            gender_mf="M",
            date_of_birth="2023-02-02",
            place_of_birth="Narra, Palawan",
            other_details="Bad dog"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data Updated Successfully", response.data)

    def test_delete(self):
        response = self.app.get("/delete/4", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Record Has Been Deleted Successfully", response.data)


if __name__ == "__main__":
    unittest.main()
