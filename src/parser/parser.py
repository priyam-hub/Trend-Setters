# PARSING THE ATTRIBUTES EXTRACTED FROM THE LLM RESPONSE

# DEPENDENCIES

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from logger.logger import LoggerSetup

# LOGGER SETUP
parser_logger = LoggerSetup(logger_name = "parser.py", log_filename_prefix = "parser").get_logger()

def parser(response : str) -> str:
    """
    Parse the structured LLM response into a standardized dictionary format.

    This function processes the raw text output from the `extractor` function (or LLM)
    and extracts predefined keys (Category, Individual_category, category_by_Gender,
    colour, MOVE_ON, FOLLOW_UP_MESSAGE). It ensures missing fields are defaulted to "NA",
    and converts the `MOVE_ON` field into a boolean.

    Arguments:

        - `response`         {str}      : The raw string response from the LLM, containing key-value pairs.

    Returns:

        - dict
            A dictionary with the following keys:
            - "Category"               : str
            - "Individual_category"    : str
            - "category_by_Gender"     : str
            - "colour"                 : str
            - "MOVE_ON"                : bool
            - "FOLLOW_UP_MESSAGE"      : str
    """
    try:

        parser_logger.info("Parsing LLM response")

        parsed_data                  = {"Category"             : "NA", 
                                        "Individual_category"  : "NA", 
                                        "category_by_Gender"   : "NA", 
                                        "colour"               : "NA", 
                                        "MOVE_ON"              : "false", 
                                        "FOLLOW_UP_MESSAGE"    : "NA"
                                        }


        current_key                  = None

        for line in response.split('\n'):
            line                     = line.strip()

            if ':' in line:
                key, value           = line.split(':', 1)
                key                  = key.strip()
                value                = value.strip().strip('"')

                if key in parsed_data:
                    parsed_data[key] = value
                    current_key      = key

            elif current_key:
                parsed_data[current_key] += ' ' + line.strip('"')

        parser_logger.debug(f"Parsed data before MOVE_ON conversion: {parsed_data}")

        parsed_data["MOVE_ON"] = parsed_data["MOVE_ON"].lower() == "true"

        parser_logger.info("LLM response parsed successfully")

        return parsed_data
    
    except Exception as e:
        parser_logger.error(f"Error parsing LLM response: {repr(e)}")
        
        raise e