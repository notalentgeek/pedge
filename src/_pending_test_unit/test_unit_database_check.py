from database          import check_db          as cd
from database          import check_doc         as cdoc
from database          import check_table       as ct
from database          import conn
from database          import create_db         as crd
from database          import create_doc        as crdoc
from database          import create_table      as crt
from database          import del_db            as dd
from exception_warning import ConventionWarning as CW
import rethinkdb as r
import sys
import unittest  as ut

class test(ut.TestCase):
    ILLEGAL_BY_RDB          = "!LLEGAL"
    ILLEGAL_BY_THIS_PROGRAM = "1LLEGAL"

    c = conn()

    """From `database.py`."""

    def test_check_db(self):
        """Test `cd()` of `check_db()` in `database.py`.

        Test 1: Assert warning for `CW` of `ConventionWarning`.
        Test 2: Assert true for database exists.
        Test 3: Assert false for database does not exists.
        Test 4: Assert true for database exist.
        """
        function_name = sys._getframe().f_code.co_name
        db_name = "{}_{}".format(function_name, "db")
        db_name_illegal_by_rdb = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_RDB
        )
        db_name_illegal_by_this_program = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = [db_name, False]
        test_list_2 = [db_name_illegal_by_rdb, False]
        test_list_3 = [db_name_illegal_by_this_program, False]

        crd(self.c, test_list_1[0])
        test_list_1[len(test_list_1) - 1] = cd(self.c, test_list_1[0])
        dd(self.c, test_list_1[0])

        test_list_2[len(test_list_2) - 1] = cd(self.c, test_list_2[0])

        r.db_create(test_list_3[0]).run(self.c)
        """Test 1."""
        with self.assertWarns(CW):
            test_list_3[len(test_list_3) - 1] = cd(self.c, test_list_3[0])
        r.db_drop(test_list_3[0]).run(self.c)

        self.assertTrue(test_list_1[len(test_list_1) - 1])  # Test 2.
        self.assertFalse(test_list_2[len(test_list_2) - 1]) # Test 3.
        self.assertTrue(test_list_3[len(test_list_3) - 1])  # Test 4.



    def test_check_table(self):
        """Test `ct()` of `check_table()` in `database.py`.

        Test 1 : Assert warning for `CW` of `ConventionWarning`.
        Test 2 : Assert warning for `CW` of `ConventionWarning`.
        Test 3 : Assert warning for `CW` of `ConventionWarning`.
        Test 4 : Assert warning for `CW` of `ConventionWarning`.
        Test 5 : Assert true for table exists.
        Test 6 : Assert false for table does not exists.
        Test 7 : Assert true for table exists.
        Test 8 : Assert false for table does not exists.
        Test 9 : Assert false for table does not exists.
        Test 10: Assert false for table does not exists.
        Test 11: Assert true for table exists.
        Test 12: Assert false for table does not exists.
        Test 13: Assert true for table exists.
        """
        function_name = sys._getframe().f_code.co_name
        db_name = "{}_{}".format(function_name, "db")
        db_name_illegal_by_rdb = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_RDB
        )
        db_name_illegal_by_this_program = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )
        table_name = "{}_{}".format(function_name, "table")
        table_name_illegal_by_rdb = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_RDB
        )
        table_name_illegal_by_this_program = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = [
            db_name,
            table_name,
            False
        ]
        test_list_2 = [
            db_name,
            table_name_illegal_by_rdb,
            False
        ]
        test_list_3 = [
            db_name,
            table_name_illegal_by_this_program,
            False
        ]
        test_list_4 = [
            db_name_illegal_by_rdb,
            table_name,
            False
        ]
        test_list_5 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_rdb,
            False
        ]
        test_list_6 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_this_program,
            False
        ]
        test_list_7 = [
            db_name_illegal_by_this_program,
            table_name,
            False
        ]
        test_list_8 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_rdb,
            False
        ]
        test_list_9 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_this_program,
            False
        ]

        crd(self.c, test_list_1[0])
        crt(self.c, test_list_1[1], test_list_1[0])
        test_list_1[len(test_list_1) - 1] = ct(
            self.c,
            test_list_1[1],
            test_list_1[0]
        )
        dd(self.c, test_list_1[0])

        test_list_2[len(test_list_2) - 1] = ct(
            self.c,
            test_list_2[1],
            test_list_2[0]
        )

        r.db_create(test_list_3[0]).run(self.c)
        r.db(test_list_3[0]).table_create(test_list_3[1]).run(self.c)
        """Test 1."""
        with self.assertWarns(CW):
            test_list_3[len(test_list_3) - 1] = ct(
                self.c,
                test_list_3[1],
                test_list_3[0]
            )
        r.db_drop(test_list_3[0]).run(self.c)

        test_list_4[len(test_list_4) - 1] = ct(
            self.c,
            test_list_4[1],
            test_list_4[0]
        )

        test_list_5[len(test_list_5) - 1] = ct(
            self.c,
            test_list_5[1],
            test_list_5[0]
        )

        test_list_6[len(test_list_6) - 1] = ct(
            self.c,
            test_list_6[1],
            test_list_6[0]
        )

        r.db_create(test_list_7[0]).run(self.c)
        r.db(test_list_7[0]).table_create(test_list_7[1]).run(self.c)
        """Test 2."""
        with self.assertWarns(CW):
            test_list_7[len(test_list_7) - 1] = ct(
                self.c,
                test_list_7[1],
                test_list_7[0]
            )
        r.db_drop(test_list_7[0]).run(self.c)

        r.db_create(test_list_8[0]).run(self.c)
        """Test 3."""
        with self.assertWarns(CW):
            test_list_8[len(test_list_8) - 1] = ct(
                self.c,
                test_list_8[1],
                test_list_8[0]
            )
        r.db_drop(test_list_8[0]).run(self.c)

        r.db_create(test_list_9[0]).run(self.c)
        r.db(test_list_9[0]).table_create(test_list_9[1]).run(self.c)
        """Test 4."""
        with self.assertWarns(CW):
            test_list_9[len(test_list_9) - 1] = ct(
                self.c,
                test_list_9[1],
                test_list_9[0]
            )
        r.db_drop(test_list_9[0]).run(self.c)

        self.assertTrue(test_list_1[len(test_list_1) - 1])  # Test 5.
        self.assertFalse(test_list_2[len(test_list_2) - 1]) # Test 6.
        self.assertTrue(test_list_3[len(test_list_3) - 1])  # Test 7.
        self.assertFalse(test_list_4[len(test_list_4) - 1]) # Test 8.
        self.assertFalse(test_list_5[len(test_list_5) - 1]) # Test 9.
        self.assertFalse(test_list_6[len(test_list_6) - 1]) # Test 10.
        self.assertTrue(test_list_7[len(test_list_7) - 1])  # Test 11.
        self.assertFalse(test_list_8[len(test_list_8) - 1]) # Test 12.
        self.assertTrue(test_list_9[len(test_list_9) - 1])  # Test 13.



    def test_check_doc(self):
        """Test `cd()` of `check_doself.c` in `database.py`.

        Test 1 : Assert warning for `CW` of `ConventionWarning`.
        Test 2 : Assert warning for `CW` of `ConventionWarning`.
        Test 3 : Assert warning for `CW` of `ConventionWarning`.
        Test 4 : Assert warning for `CW` of `ConventionWarning`.
        Test 5 : Assert true for document exists.
        Test 6 : Assert false for document does not exists.
        Test 7 : Assert true for document exists.
        Test 8 : Assert false for document does not exists.
        Test 9 : Assert false for document does not exists.
        Test 10: Assert false for document does not exists.
        Test 11: Assert true for document exists.
        Test 12: Assert false for document does not exists.
        Test 13: Assert true for document exists.
        """
        function_name = sys._getframe().f_code.co_name
        db_name = "{}_{}".format(function_name, "db")
        db_name_illegal_by_rdb = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_RDB
        )
        db_name_illegal_by_this_program = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )
        table_name = "{}_{}".format(function_name, "table")
        table_name_illegal_by_rdb = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_RDB
        )
        table_name_illegal_by_this_program = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )
        doc_1 = {"name": "alpha", "no":"1"}

        test_list_1 = [
            db_name,
            table_name,
            doc_1,
            False
        ]
        test_list_2 = [
            db_name,
            table_name_illegal_by_rdb,
            doc_1,
            False
        ]
        test_list_3 = [
            db_name,
            table_name_illegal_by_this_program,
            doc_1,
            False
        ]
        test_list_4 = [
            db_name_illegal_by_rdb,
            table_name,
            doc_1,
            False
        ]
        test_list_5 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_rdb,
            doc_1,
            False
        ]
        test_list_6 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_this_program,
            doc_1,
            False
        ]
        test_list_7 = [
            db_name_illegal_by_this_program,
            table_name,
            doc_1,
            False
        ]
        test_list_8 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_rdb,
            doc_1,
            False
        ]
        test_list_9 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_this_program,
            doc_1,
            False
        ]

        crd(self.c, test_list_1[0])
        crt(self.c, test_list_1[1], test_list_1[0])
        crdoc(self.c, test_list_1[2], test_list_1[1], test_list_1[0])
        test_list_1[len(test_list_1) - 1] = cdoc(
            self.c,
            test_list_1[2]["name"],
            "name",
            test_list_1[1],
            test_list_1[0]
        )
        dd(self.c, test_list_1[0])

        r.db_create(test_list_2[0]).run(self.c)
        test_list_2[len(test_list_2) - 1] = cdoc(
            self.c,
            test_list_2[2]["name"],
            "name",
            test_list_2[1],
            test_list_2[0]
        )
        r.db_drop(test_list_2[0]).run(self.c)

        r.db_create(test_list_3[0]).run(self.c)
        r.db(test_list_3[0]).table_create(test_list_3[1]).run(self.c)
        r.db(test_list_3[0]).table(test_list_3[1]).insert(test_list_3[2])\
            .run(self.c)
        """Test 1."""
        with self.assertWarns(CW):
            test_list_3[len(test_list_3) - 1] = cdoc(
                self.c,
                test_list_3[2]["name"],
                "name",
                test_list_3[1],
                test_list_3[0]
            )
        r.db_drop(test_list_3[0]).run(self.c)

        test_list_4[len(test_list_4) - 1] = cdoc(
            self.c,
            test_list_4[2]["name"],
            "name",
            test_list_4[1],
            test_list_4[0]
        )

        test_list_5[len(test_list_5) - 1] = cdoc(
            self.c,
            test_list_5[2]["name"],
            "name",
            test_list_5[1],
            test_list_5[0]
        )

        test_list_6[len(test_list_6) - 1] = cdoc(
            self.c,
            test_list_6[2]["name"],
            "name",
            test_list_6[1],
            test_list_6[0]
        )

        r.db_create(test_list_7[0]).run(self.c)
        r.db(test_list_7[0]).table_create(test_list_7[1]).run(self.c)
        r.db(test_list_7[0]).table(test_list_7[1]).insert(test_list_7[2])\
            .run(self.c)
        """Test 2."""
        with self.assertWarns(CW):
            test_list_7[len(test_list_7) - 1] = cdoc(
                self.c,
                test_list_7[2]["name"], 
                "name",
                test_list_7[1],
                test_list_7[0]
            )
        r.db_drop(test_list_7[0]).run(self.c)

        r.db_create(test_list_8[0]).run(self.c)
        """Test 3."""
        with self.assertWarns(CW):
            test_list_8[len(test_list_8) - 1] = cdoc(
                self.c,
                test_list_8[2]["name"],
                "name",
                test_list_8[1],
                test_list_8[0]
            )
        r.db_drop(test_list_8[0]).run(self.c)

        r.db_create(test_list_9[0]).run(self.c)
        r.db(test_list_9[0]).table_create(test_list_9[1]).run(self.c)
        r.db(test_list_9[0]).table(test_list_9[1]).insert(test_list_9[2])\
            .run(self.c)
        """Test 4."""
        with self.assertWarns(CW):
            test_list_9[len(test_list_9) - 1] = cdoc(
                self.c,
                test_list_9[2]["name"],
                "name",
                test_list_9[1],
                test_list_9[0]
            )
        r.db_drop(test_list_9[0]).run(self.c)

        self.assertTrue(test_list_1[len(test_list_1) - 1])  # Test 5.
        self.assertFalse(test_list_2[len(test_list_2) - 1]) # Test 6.
        self.assertTrue(test_list_3[len(test_list_3) - 1])  # Test 7.
        self.assertFalse(test_list_4[len(test_list_4) - 1]) # Test 8.
        self.assertFalse(test_list_5[len(test_list_5) - 1]) # Test 9.
        self.assertFalse(test_list_6[len(test_list_6) - 1]) # Test 10.
        self.assertTrue(test_list_7[len(test_list_7) - 1])  # Test 11.
        self.assertFalse(test_list_8[len(test_list_8) - 1]) # Test 12.
        self.assertTrue(test_list_9[len(test_list_9) - 1])  # Test 13.

if __name__ == "__main__":
    ut.main()