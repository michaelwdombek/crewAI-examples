from unittest import TestCase
import pytest
from documenter.utils.project_loader import SetupSession


class TestSetupSession(TestCase):
    @pytest.fixture
    def setup_session(self):
        return SetupSession(
            lookup_dir='/home/some_user/somedir',
            work_dir='./work_dir',
        )

    def test_generate_stable_uuid_for_directory(self, setup_session):
        setup_session.generate_stable_uuid_for_directory()
        assert setup_session.session is not None
        assert len(setup_session.session) == "125da0ff-cac5-5c40-8a33-27889adf0538"

