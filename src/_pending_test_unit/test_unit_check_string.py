from check_string import check_name_client as ccn
from check_string import check_db_host     as cdh
from check_string import check_db_name     as cdn
from check_string import check_table_name  as ctn
import unittest as ut

class test(ut.TestCase):

    """From `check_string.py`."""

    def test_check_name_client(self):
        true = [
            "client", "client1", "client1A", "client1Alpha", "clientA",
            "clientA1", "clientAlpha", "clientAlpha1"
        ]

        false = [
            " client Alpha ", " Client Alpha ", " client alpha ",
            " Client alpha ", "!client!Alpha!", "!client!alpha!",
            "!Client!Alpha!", "!Client!alpha!", "_client_Alpha_",
            "_client_alpha_", "_Client_Alpha_", "_Client_alpha_",
            "client Alpha", "client alpha", "Client Alpha", "Client alpha",
            "client!Alpha", "client!alpha", "Client!Alpha", "Client!alpha",
            "client_Alpha", "client_alpha", "Client_Alpha", "Client_alpha"
        ]

        for i in true:
            self.assertTrue(ccn(i))

        for i in false:
            self.assertFalse(ccn(i))



    def test_check_db_host(self):
            "0.0.0.0", "127.0.0.1", "255.255.255.255", "http://localhost",
            "http://localhost/", "https://localhost", "https://localhost/",
            "localhost"
        ]

        false = [
            "-1.-1.-1.-1", "127.  0.0.1", "127. 0. 0. 1", "127. 0. 0.1",
            "127. 0.0.1", "256.256.256.256", "https://google.com"
        ]

        for i in true:
            self.assertTrue(cdh(i))

        for i in false:
            self.assertFalse(cdh(i))

        self.assertFalse(cdh("http://localhost/", False))
        self.assertFalse(cdh("https://localhost/", False))



    def test_check_db_name(self):
        true = [
            "db", "db_1", "db_alpha", "db_alpha_1", "dbalpha", "dbalpha_1"
        ]

        false = [
            " db ", " Db ", " db 1 ", " Db 1 ", " db alpha ", " Db alpha ",
            " db alpha 1 ", " Db alpha 1 ", "db!", "Db!", "db!alpha",
            "db!Alpha", "Db!alpha", "Db!Alpha", "db!alpha!1", "db!Alpha!1",
            "Db!alpha!1", "Db!Alpha!1", "db1", "Db1", "dbAlpha", "DbAlpha",
            "dbAlpha1", "DbAlpha1"
        ]

        for i in true:
            self.assertTrue(cdn(i))

        for i in false:
            self.assertFalse(cdn(i))



    def test_check_table_name(self):
        true = [
            "table", "table_alpha", "table_1", "tableAlpha", "tableAlpha_1",
            "table_alpha_1"
        ]

        false = [
            " table ", " Table ", " table1 ", " Table1 ", "!table!",
            "!Table!", "!table!1!", "!Table!1!", "table1", "Table1"
        ]

        for i in true:
            self.assertTrue(ctn(i))

        for i in false:
            self.assertFalse(ctn(i))

            true = [

if __name__ == "__main__":
    ut.main()