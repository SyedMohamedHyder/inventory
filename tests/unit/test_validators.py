"""

Unittests for all the validators in app/utils/validators.py

"""

import pytest
from app.utils.validators import validate_integer


class TestIntegerValidator:
    """

    Tests for the validate_integer function

    """

    def test_valid(self):
        """

        Test for a valid data passed to validate_integer

        """

        validate_integer('arg', 5, 0, 10, 'custom', 'custom')

    def test_type_error(self):
        """

        Test to check whether validate_integer raises a `TypeError` for an invalid type passed to arg_value

        """

        with pytest.raises(TypeError):
            validate_integer('arg', 1.5, 0, 5, 'custom', 'custom')

    def test_min_default_error_msg(self):
        """

        Test to check whether default msg is proper when the `ValueError` is raised

        """

        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 5, 10, 20)
        assert 'arg' in str(ex.value)
        assert '10' in str(ex.value)

    def test_min_custom_error_msg(self):
        """

        Test to check whether custom msg is present in the `ValueError` message when it is raised

        """

        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 5, 10, 20, 'custom_min', 'custom_max')
        assert str(ex.value) == 'custom_min'

    def test_max_default_error_msg(self):
        """

        Test to check whether default msg is proper when the `ValueError` is raised

        """

        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 25, 10, 20)
        assert 'arg' in str(ex.value)
        assert '20' in str(ex.value)

    def test_max_custom_error_msg(self):
        """

        Test to check whether custom msg is present in the `ValueError` message when it is raised

        """

        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 25, 10, 20, 'custom_min', 'custom_max')
        assert str(ex.value) == 'custom_max'
