from database          import conn
from exception_warning import ConventionWarning       as CW
import sys
import unittest  as ut

class test(ut.TestCase):
    ILLEGAL_BY_RDB          = "!LLEGAL"
    ILLEGAL_BY_THIS_PROGRAM = "1LLEGAL"

    """From `database.py`."""

    def test_conn(self):
        """Test `conn()` in `database.py`.

        Test 1: Assert warning for `CW` of `ConventionWarning`.
        Test 2: Assert warning for `CW` of `ConventionWarning`.
        Test 3: Assert not none for valid `conn()` object.
        Test 4: Assert none for counterfeit `conn()` object.
        Test 5: Assert none for counterfeit `conn()` object.
        """
        function_name = sys._getframe().f_code.co_name
        db_host = "{}_{}".format(function_name, "host")
        db_host_illegal_by_rdb = "{}_{}".format(
            db_host,
            self.ILLEGAL_BY_RDB
        )
        db_host_illegal_by_this_program = "{}_{}".format(
            db_host,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = None
        test_list_2 = [db_host_illegal_by_rdb, None]
        test_list_3 = [db_host_illegal_by_this_program, None]

        test_list_1 = conn()

        """Test 1."""
        with self.assertWarns(CW):
                test_list_2[len(test_list_2) - 1] = conn(db_host_illegal_by_rdb)

        """Test 2."""
        with self.assertWarns(CW):
                test_list_3[len(test_list_3) - 1] = conn(
                    db_host_illegal_by_this_program
                )

        self.assertIsNotNone(test_list_1)                    # Test 3.
        self.assertIsNone(test_list_2[len(test_list_2) - 1]) # Test 4.
        self.assertIsNone(test_list_3[len(test_list_3) - 1]) # Test 5.

if __name__ == "__main__":
    ut.main()