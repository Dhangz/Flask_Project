import unittest
from api import app
import warnings

class MyappTests(unittest.TestCase):
  def setUp(self):
    app.config["TESTING"] = True
    self.app = app.test_client()


    warnings.simplefilter("ignore", category=DeprecationWarning)
    
  def test_index_page(self):
    response = self.app.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

  def test_get_dogs(self):
    response = self.app.get("/dogs")
    self.assertEqual(response.status_code, 200)
    self.assertTrue("Loxodonta africana" in response.data.decode())

  def test_get_dog_by_id(self):
    response = self.app.get("/dogs/1")
    self.assertEqual(response.status_code, 200)
    self.assertTrue("Loxodonta africana" in response.data.decode())





if __name__ == "__main__":
  unittest.main()