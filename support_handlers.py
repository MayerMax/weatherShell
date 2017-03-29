import sys


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
