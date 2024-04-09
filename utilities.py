import json
from sciform import SciNum


# Load JSON data from a file
def load_json_file(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


# Validate the structure of the data
def validate_data(data):
    if not isinstance(data, list):
        raise ValueError("Data is not a list")

    for engine in data:
        if not isinstance(engine, dict):
            raise ValueError("Engine data is not an object")

        # Check for required keys and their types
        required_keys = {
            "name": str,
            "thrust": list,
            "isp": list,
        }
        for key, expected_type in required_keys.items():
            if key not in engine:
                raise ValueError(f"Missing required key: {key} in engine")
            if not isinstance(engine[key], expected_type):
                raise ValueError(
                    f"Incorrect type for key: {key}, expected {expected_type.__name__} in engine"
                )

            # Additional validation for lists to ensure they contain numbers
            if expected_type is list:
                if not all(isinstance(item, float or int) for item in engine[key]):
                    raise ValueError(
                        f"All items in {key} must be of type Number in engine"
                    )
                if key in ["thrust", "isp"] and len(engine[key]) != 2:
                    raise ValueError(
                        f"{key} must contain exactly two elements in engine"
                    )


def load_data(filename):
    try:
        loaded_data = load_json_file(filename)
        validate_data(loaded_data)
        print("Data loaded and validated successfully.")
    except Exception as e:
        print(f"Error: {e}")


def print_result(value, unit, precision=4):
    # Using formatting mini language from sciform to achieve deesired engineering notation.
    # https://sciform.readthedocs.io/en/stable/fsml.html
    formatted_value = f"{SciNum(value):#!{precision}rp}"
    print(f"{formatted_value}{unit}")


if __name__ == "__main__":
    filename = "engines.json"
    load_data(filename)
