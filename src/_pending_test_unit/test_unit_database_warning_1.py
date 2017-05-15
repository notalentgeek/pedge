from database          import cdw_db_creation_mod     as cdw_dcm
from database          import cdw_db_deletion_mod     as cdw_ddm
from database          import cdw_table_creation_mod  as cdw_tcm
from database          import cdw_table_deletion_mod  as cdw_tdm
from database          import cw_db_mod               as cwdm
from database          import cw_table_mod            as cwtm
from exception_warning import ConventionWarning       as CW
from exception_warning import CreationDeletionWarning as CDW
import unittest as ut
import warnings as warn

class test(ut.TestCase):
    ANY_STRING = "any" # LOL Mikael pls.

    """From `database.py`."""

    def test_cw_db_mod(self):
        """Test `cwdm()` of `cw_database_mod()` in `database.py`.

        Test 1: Assert warning for `CW` of `ConventionWarning`.
        """
        test_list_1 = self.ANY_STRING
        
        """Test 1."""
        with self.assertWarns(CW):
            cwdm(test_list_1) 



    def test_cw_table_mod(self):
        """Test `cwtm()` of `cw_table_mod()` in `database.py`.

        Test 1. Assert warning for `CW` of `ConventionWarning`.
        """
        test_list_1 = self.ANY_STRING
        
        """Test 1."""
        with self.assertWarns(CW):
            cwtm(test_list_1) 



    def test_cdw_db_creation_mod(self):
        """Test `cdw_dcm()` of `cdw_db_creation_mod()` in `database.py`.

        Test 1. Assert warning for `CDW` of `CreationDeletionWarning`.
        """
        test_list_1 = self.ANY_STRING
        
        """Test 1."""
        with self.assertWarns(CDW):
            cdw_dcm(test_list_1)



    def test_cdw_db_deletion_mod(self):
        """Test `cdw_ddm()` of `cdw_db_deletion_mod()` in `database.py`.

        Test 1. Assert warning for `CDW` of `CreationDeletionWarning`.
        """
        test_list_1 = self.ANY_STRING
        
        """Test 1."""
        with self.assertWarns(CDW):
            cdw_ddm(test_list_1)



    def test_cdw_table_creation_mod(self):
        """Test `cdw_tcm()` of `cdw_table_creation_mod()` in `database.py`.

        Test 1. Assert warning for `CDW` of `CreationDeletionWarning`.
        """
        test_list_1 = self.ANY_STRING
        
        """Test 1."""
        with self.assertWarns(CDW):
            cdw_tcm(test_list_1)



    def test_cdw_table_deletion_mod(self):
        """Test `cdw_tdm()` of `cdw_table_deletion_mod()` in `database.py`.

        Test 1. Assert warning for `CDW` of `CreationDeletionWarning`.
        """
        test_list_1 = self.ANY_STRING
        
        """Test 1."""
        with self.assertWarns(CDW):
            cdw_tdm(test_list_1)

if __name__ == "__main__":
    ut.main()