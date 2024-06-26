import requests
import os
from dotenv import load_dotenv
import pytest
from datetime import datetime, timedelta

from sylveon._classes._login_helpers import (
    login_set_session_cookies,
    get_auth_token_init_gradescope_session,
)

from sylveon._classes._connection import GSConnection

from sylveon._classes._extensions import get_extensions, update_student_extension

# load .env file
load_dotenv()

GRADESCOPE_CI_STUDENT_EMAIL = os.getenv("GRADESCOPE_CI_STUDENT_EMAIL")
GRADESCOPE_CI_STUDENT_PASSWORD = os.getenv("GRADESCOPE_CI_STUDENT_PASSWORD")
GRADESCOPE_CI_INSTRUCTOR_EMAIL = os.getenv("GRADESCOPE_CI_INSTRUCTOR_EMAIL")
GRADESCOPE_CI_INSTRUCTOR_PASSWORD = os.getenv("GRADESCOPE_CI_INSTRUCTOR_PASSWORD")


def new_session(account_type="student"):
    """Creates and returns a session for testing"""
    connection = GSConnection()

    match account_type.lower():
        case "student":
            connection.login(
                GRADESCOPE_CI_STUDENT_EMAIL, GRADESCOPE_CI_STUDENT_PASSWORD
            )
        case "instructor":
            connection.login(
                GRADESCOPE_CI_INSTRUCTOR_EMAIL, GRADESCOPE_CI_INSTRUCTOR_PASSWORD
            )
        case _:
            raise ValueError("Invalid account type: must be 'student' or 'instructor'")

    return connection.session


# @pytest.mark.skip("Not implemented")
def test_get_extensions():
    # create test session
    test_session = requests.Session()

    # assuming test_get_auth_token_init_gradescope_session works
    auth_token = get_auth_token_init_gradescope_session(test_session)
    login_check = login_set_session_cookies(
        test_session,
        GRADESCOPE_CI_INSTRUCTOR_EMAIL,
        GRADESCOPE_CI_INSTRUCTOR_PASSWORD,
        auth_token,
    )

    course_id = "753413"
    assignment_id = "4330410"
    extensions = get_extensions(test_session, course_id, assignment_id)
    print(extensions)


def test_valid_change_extension():
    """Test valid extension for a student."""
    # create test session
    test_session = requests.Session()

    # assuming test_get_auth_token_init_gradescope_session works
    auth_token = get_auth_token_init_gradescope_session(test_session)
    login_check = login_set_session_cookies(
        test_session,
        GRADESCOPE_CI_INSTRUCTOR_EMAIL,
        GRADESCOPE_CI_INSTRUCTOR_PASSWORD,
        auth_token,
    )

    course_id = "753413"
    assignment_id = "4330410"
    user_id = "6515875"
    release_date = datetime(2024, 4, 15)
    due_date = release_date + timedelta(days=1)
    late_due_date = due_date + timedelta(days=1)

    result = update_student_extension(
        test_session,
        course_id,
        assignment_id,
        user_id,
        release_date,
        due_date,
        late_due_date,
    )
    assert result


def test_invalid_change_extension():
    """Test invalid extension dates for a student."""
    # create test session
    test_session = requests.Session()

    # assuming test_get_auth_token_init_gradescope_session works
    auth_token = get_auth_token_init_gradescope_session(test_session)
    login_check = login_set_session_cookies(
        test_session,
        GRADESCOPE_CI_INSTRUCTOR_EMAIL,
        GRADESCOPE_CI_INSTRUCTOR_PASSWORD,
        auth_token,
    )

    course_id = "753413"
    assignment_id = "4330410"
    user_id = "6515875"
    release_date = datetime(2024, 4, 15)
    due_date = release_date + timedelta(days=-1)
    late_due_date = due_date + timedelta(days=-1)

    with pytest.raises(
        ValueError,
        match="Dates must be in order: release_date <= due_date <= late_due_date",
    ):
        update_student_extension(
            test_session,
            course_id,
            assignment_id,
            user_id,
            release_date,
            due_date,
            late_due_date,
        )


# Todo:
# invalid user id?
# invalid assignment id?
# invalid course id?
