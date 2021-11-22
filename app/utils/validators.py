"""

Various validators

"""


def validate_integer(arg_name, arg_value, min_value=None, max_value=None,
                     custom_min_msg=None, custom_max_msg=None):
    """
    Validates whether the `arg_value` is an integer and also checks if it falls within the specified bounds if the
    min_value and max_value are provided.

    Custom override error messages can be passed, that will be raised when arg_value exceeds the specified bounds

    Args:
        arg_name (str): the name of the argument that will be used in the default error messages
        arg_value (obj): the value being validated
        min_value (int): optional, specifies the min value (inclusive)
        max_value (int): optional, specifies the max value (inclusive)
        custom_min_msg (str): optional, custom message when value is less than minimum
        custom_max_msg (str): optional, custom message when value is greater than maximum

    Returns:
        None: no exceptions will be raised if validation passes

    Raises:
        TypeError: if `arg_value` is not an integer
        ValueError: if `arg_value` is not within the bounds

    """

    if not isinstance(arg_value, int):
        raise TypeError(f'{arg_name} must be an integer')

    if min_value is not None and arg_value < min_value:
        if custom_min_msg is not None:
            raise ValueError(custom_min_msg)
        raise ValueError(f'{arg_name} cannot be less than {min_value}')

    if max_value is not None and arg_value > max_value:
        if custom_max_msg is not None:
            raise ValueError(custom_max_msg)
        raise ValueError(f'{arg_name} cannot be greater than {max_value}')
