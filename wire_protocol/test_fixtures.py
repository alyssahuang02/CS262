import pytest


@pytest.fixture
def register_message():
    return "!PURPOSE:/!REGISTER/!LENGTH:/4/!BODY:/dale"


@pytest.fixture
def login_message():
    return "!PURPOSE:/!LOGIN/!LENGTH:/4/!BODY:/dale"


@pytest.fixture
def show_accounts_message():
    return "!PURPOSE:/!SHOWACCOUNTS/!LENGTH:/4/!BODY:/dale"


@pytest.fixture
def check_user_exists_message():
    return "!PURPOSE:/!CHECKUSEREXISTS/!LENGTH:/4/!BODY:/dale"


@pytest.fixture
def pull_message():
    return "!PURPOSE:/!PULL/!LENGTH:/1/!BODY:/ "


@pytest.fixture
def delete_account_message():
    return "!PURPOSE:/!DELETEACCOUNT/!LENGTH:/4/!BODY:/dale"


@pytest.fixture
def logout_message():
    return "!PURPOSE:/!LOGOUT/!LENGTH:/4/!BODY:/dale"


@pytest.fixture
def receive_single_message():
    return "!PURPOSE:/!NOTIFY/!LENGTH:/21/!BODY:/alyssa sends: hi dale"


@pytest.fixture
def receive_no_more_data():
    return "!PURPOSE:/!NOMOREDATA/!LENGTH:/1/!BODY:/ "


@pytest.fixture
def notify_message_login_successful():
    return "!PURPOSE:/!NOTIFY/!LENGTH:/17/!BODY:/Login successful!"


@pytest.fixture
def send_single_message():
    return ["!PURPOSE:/!NOTIFY/!LENGTH:/21/!BODY:/alyssa sends: hi dale", "!PURPOSE:/!NOMOREDATA/!LENGTH:/1/!BODY:/ "]
