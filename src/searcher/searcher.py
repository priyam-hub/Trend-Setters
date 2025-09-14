# SEARCH FUNCTION USING QDRANT CLIENT

# DEPENDENCIES

import os
import sys
import random
from math import e
from re import search
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import warnings
warnings.filterwarnings(action = "ignore")

from logger.logger import LoggerSetup

# LOGGER SETUP
searcher_logger = LoggerSetup(logger_name = "searcher.py", log_filename_prefix = "searcher").get_logger()

def search_collection(client               : object,
                      collection_name      :str, 
                      colour               : str = "NA",
                      individual_category  : str = "NA",
                      category             : str = "NA",
                      category_by_gender   : str = "NA"
                      ) -> list:
    """
    Search and retrieve items from a Qdrant collection based on optional filtering attributes.

    This function scrolls through all points in the specified Qdrant collection and
    applies dynamic filters (colour, individual_category, category, category_by_gender).
    If filters are provided, only matching items are returned. If no filters are provided,
    10 random items are sampled and returned. If filters yield no results, 10 random
    items are returned as a fallback.

    Arguments:

        - `colour`                {str, optional}      : Filter results by the `colour` attribute.
                                                         If "NA", this filter is ignored.

        - `individual_category`   {str, optional}      : Filter results by the `Individual_category` attribute.
                                                         If "NA", this filter is ignored.

        - `category`              {str, optional}      : Filter results by the `Category` attribute.
                                                         If "NA", this filter is ignored.

        - `category_by_gender`    {str, optional}      : Filter results by the `category_by_Gender` attribute.
                                                         If "NA", this filter is ignored.

    Returns

        - `results`                   {list}           : A list of payload dictionaries representing the filtered or
                                                         randomly sampled items from the collection.
    """

    try:

        # CONSTRUCT FILTER LOGIC BASED ON THE ATTRIBUTES
        filters                  = []

        if colour               != "NA":
            filters.append(lambda point: point.payload.get("colour") == colour)

        if individual_category  != "NA":
            filters.append(lambda point: point.payload.get("Individual_category") == individual_category)

        if category             != "NA":
            filters.append(lambda point: point.payload.get("Category") == category)

        if category_by_gender   != "NA":
            filters.append(lambda point: point.payload.get("category_by_Gender") == category_by_gender)

        # RETRIEVE AND FILTER POINTS
        all_points               = []
        next_page                = None

        searcher_logger.info(f"Searching the collection with filters - colour: {colour}, individual_category: {individual_category}, category: {category}")

        while True:
            response, next_page  = client.scroll(collection_name  = collection_name,
                                                limit            = 1000,
                                                offset           = next_page
                                                )
            all_points.extend(response)

            if not next_page:
                break

        # FILTERED POINTS
        if filters:
            filtered_points = [point for point in all_points
                            if all(f(point) for f in filters)
                            ]
            
            searcher_logger.info(f"Number of points after applying filters: {len(filtered_points)}")

        # RANDOM 10 POINTS IF NO FILTERS IS APPLIED
        else:
            filtered_points = random.sample(all_points, min(10, len(all_points)))

            searcher_logger.info(f"No filters applied. Randomly selected {len(filtered_points)} points.")

        # OUTPUT OF THE RESULTS
        if filtered_points:
            results         = [point.payload for point in filtered_points]

            searcher_logger.info(f"Number of points returned: {len(results)}")

        else:
            random_points   = random.sample(all_points, min(10, len(all_points)))
            results         = [point.payload for point in random_points]

            searcher_logger.info(f"No points matched the filters. Randomly selected {len(results)} points as fallback.")

        return results
    
    except Exception as e:
        searcher_logger.error(f"Error in searching the collection: {repr(e)}")
        
        return []