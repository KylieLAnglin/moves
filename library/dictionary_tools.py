# %% Functions
def fold_nested_dictionary(input_dict: dict, inner_key: str):
    """Given an input dictionary with keys mapping to inner dictionaries, extract
        the value of some common key to the inner dictionary and return the new
        "folded" dictionary.

    Arguments:
        input_dict (Dict[Any, Dict[str, Any]]): The input dictionary containing dictionaries as values
        inner_key (str): The key to use to extract a given value out of the inner dictionaries.

    Returns:
        A new "folded" dictionary consisting of the original dictionary's keys and the values of the inner_key.
    """
    return {k: v[inner_key] for k, v in input_dict.items()}


def replace_string_value_as_list(input_dict: dict):
    """Given an input dictionary, replace string values with list of one string

    Args:
        input_dict (dict): Dictionary containing string values

    Returns:
        [type]: Dictionary containing list values of one item each
    """
    return {k: [v] for k, v in input_dict.items()}


def replace_string_key(input_dict: dict, old_str: str, new_str: str):
    """Replaces substring in dictionary key values

    Args:
        input_dict (dict): dictionary with string as key
        old_str (str): old substring to replace
        new_str (str): new substring

    Returns:
        [dict]: dictionary with replaced substrings in keys
    """
    return {k.replace(old_str, new_str): v for k, v in input_dict.items()}


def string_key_as_int(input_dict: dict):
    """new dictionary with string keys converted to int

    Args:
        input_dict (dict): input dictionary with string keys

    Returns:
        [dict]: new dictionary with int keys
    """
    return {int(k): v for k, v in input_dict.items()}


test = {
    "misbehavior": ["hum", "humming"],
    "avatar": ["Ethan"],
}
result = {"hum": "misbehavior", "humming": "misbehavior", "Ethan": "avatar"}


def long_inverse_dict_from_key_list(input_dict: dict):
    """Given dict with list in values, create new dict with entry for term in lists with key now value

    Args:
        input_dict (dict): Dictionary with list as values

    Returns:
        new_dict (dict): Dictionary with key for every value in old dict
    """
    new_dict = {}
    for key, value in input_dict.items():
        for entry in value:
            new_dict[entry] = key

    return new_dict


result = long_inverse_dict_from_key_list(test)
