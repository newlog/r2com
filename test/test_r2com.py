from r2com import R2COM
import unittest
import os


class TestR2COM(unittest.TestCase):

  def setUp(self):
    self.lab7_2_binary = os.path.join(os.path.dirname(__file__), '..', 'bin', 'Lab07-02.exe')

  def test_basic_case(self):
    r2com = R2COM(self.lab7_2_binary)
    success = r2com.execute()
    self.assertTrue(success)

  def test_get_cocreateinstance_clsids(self):
    r2com = R2COM(self.lab7_2_binary)
    clsid_info = r2com.get_cocreateinstance_clsids()
    self.assertEqual(clsid_info, {4198429:  # push instruction address (where the comment is added)
                                    {
                                      'clsid_addr': 4202584,  # address where the clsid structure is stored (address pushed as parameter to CoCreate)
                                      'clsid': '{0002df01-0000-0000-c000-000000000046}'  # CLSID value
                                    }
                                  })

