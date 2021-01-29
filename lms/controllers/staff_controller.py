from flask import session

import database


def create_staff_from_cursor(cursor):
    """
    Returns a Staff object populated with data from a pymongo cursor

    Parameters
    ----------
    cursor : pymongo_cursor
    Database information to load into staff object

    Returns
    -------
    Staff Object on success
    Empty dict on failure
    """

    s = {}
    if cursor:
        s = Staff(cursor['_id'],
                    cursor['forename'],
                    cursor['surname'],
                    cursor['profile_about'],
                    cursor['profile_image'],
                    cursor['subjects'])

    return s



