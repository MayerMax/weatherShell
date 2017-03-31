import sys
import dbm


def print_auto_complete_variants(possible_values):
    print("_____________________")
    print("Sorry, your query is not precise, here are the variants, "
          "by autocomplete:\n")
    for v in possible_values:
        print(v.name, v.c_c)
    print("____________________")


def assert_ascii(given_name):
    try:
        given_name.encode("ascii")
        return given_name
    except UnicodeEncodeError as unicode_error:
        print("Sorry, ascii symbols supported only")
        sys.exit()


class DataBase:
    def __init__(self):
        self.db = "records"

    def add_record(self, string_name, string_description):
        with dbm.open(self.db, "c") as db:
            if string_name.encode() in db.keys():
                return False
            db[string_name] = string_description
            return True

    def get_record(self, string_name):
        with dbm.open(self.db, "c") as db:
            if string_name.encode() in db.keys():
                return db[string_name].decode()

    def get_records_count(self):
        with dbm.open(self.db, "c") as db:
            return len(db)

    def delete_record(self, string_name):
        with dbm.open(self.db, "c") as db:
            if string_name.encode() in db.keys():
                del db[string_name.encode()]
                return True
        return False

    def retrieve_past_queries(self):
        with dbm.open(self.db, "c") as db:
            return "".join(db[x].decode() for x in db.keys())






