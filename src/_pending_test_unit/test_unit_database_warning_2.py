from database          import cdw_prevent_creation_or_deletion_if_string_check_fail as prevent_cd
from exception_warning import CreationDeletionWarning                               as CDW
import sys
import unittest as ut
import warnings as warn

class test(ut.TestCase):
    ANY_STRING = "any" # LOL Mikael pls.

    """From `database.py`."""

    def test_cdw_prevent_creation_or_deletion_if_string_check_fail(self):
        """Test `prevent_cd()` of
        `cdw_prevent_creation_or_deletion_if_string_check_fail()` in
        `database.py`.

        Test 1: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 2: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 3: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 4: Assert warning for `CDW` of `CreationDeletionWarning`.
        """

        test_list_1 = [self.ANY_STRING, True , True ]
        test_list_2 = [self.ANY_STRING, True , False]
        test_list_3 = [self.ANY_STRING, False, True ]
        test_list_4 = [self.ANY_STRING, False, False]

        """Test 1."""
        with self.assertWarns(CDW):
            prevent_cd(test_list_1[0], test_list_1[1], test_list_1[2])

        """Test 2."""
        with self.assertWarns(CDW):
            prevent_cd(test_list_2[0], test_list_2[1], test_list_2[2])

        """Test 3."""
        with self.assertWarns(CDW):
            prevent_cd(test_list_3[0], test_list_3[1], test_list_3[2])

        """Test 4."""
        with self.assertWarns(CDW):
            prevent_cd(test_list_4[0], test_list_4[1], test_list_4[2])

if __name__ == "__main__":
    ut.main()