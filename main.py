# MAIN FUNCTION

# DEPENDENCIES

import os
from pyexpat import model
import sys
from ast import main
from re import search
from pathlib import Path
from urllib import response
from dotenv import load_dotenv
from huggingface_hub import login
from qdrant_client import QdrantClient

from src.parser.parser import parser
from src.extractor.extractor import extractor
from src.llm.llm_builder import initialize_hf_llm
from src.searcher.searcher import search_collection
# from src.llm.llm_builder import initialize_chatgroq_llm

import warnings
warnings.filterwarnings(action = "ignore")

# LOADING ENVIRONMENT VARIABLES
load_dotenv()

GROQ_API_KEY                = os.environ.get('GROQ_API_KEY')
LLM_MODEL_NAME              = os.environ.get('LLM_MODEL_NAME')
QDRANT_API_KEY              = os.environ.get('QDRANT_API_KEY')
QDRANT_CLUSTER_URL          = os.environ.get('QDRANT_CLUSTER_URL')
QDRANT_COLLECTION_NAME      = os.environ.get('QDRANT_COLLECTION_NAME')
HF_LLM_MODEL_NAME           = os.environ.get('HF_LLM_MODEL_NAME')
HUGGINGFACE_LOGIN_TOKEN     = os.environ.get('HUGGINGFACE_LOGIN_TOKEN')

from logger.logger import LoggerSetup

# LOGGER SETUP
main_logger                 = LoggerSetup(logger_name = "main.py", log_filename_prefix = "main").get_logger()


def main():
    # INITIALIZING THE QDRANT CLIENT
    client                  = QdrantClient(url      = QDRANT_CLUSTER_URL, 
                                           api_key  = QDRANT_API_KEY
                                           )

    main_logger.info("Qdrant client initialized successfully")

    main_logger.info(f"GROQ_API_KEY : {'Present' if GROQ_API_KEY else 'Not Present'}")
    main_logger.info(f"LLM_MODEL_NAME : {LLM_MODEL_NAME if LLM_MODEL_NAME else 'Not Present'}")

    # llm                     = initialize_chatgroq_llm(temperature   = 0.5, 
    #                                                   groq_api_key  = GROQ_API_KEY, 
    #                                                   model_name    = LLM_MODEL_NAME
    #                                                   )

    # main_logger.info("ChatGroq LLM initialized successfully")

    login(HUGGINGFACE_LOGIN_TOKEN)

    llm                     = initialize_hf_llm(hf_llm_model_name   = HF_LLM_MODEL_NAME, 
                                                temperature         = 0.5, 
                                                max_new_tokens      = 512, 
                                                do_sample           = True,
                                                use_lora            = True,
                                                lora_r              = 8,
                                                lora_alpha          = 16,
                                                lora_dropout        = 0.05,
                                                lora_target_modules = ["q_proj", "v_proj"]
                                                )

    main_logger.info("Fine-Tuned LLM initialized successfully")

    conversation            = "I need black women jeans"
    extractor_response      = extractor(llm                   = llm, 
                                        conversation_history  = conversation
                                        )

    main_logger.info(f"Extractor response: {extractor_response}")

    response                = parser(response = extractor_response)
    main_logger.info(f"Parser response: {response}")

    # search_results          = search_collection(client               = client,
    #                                             collection_name      = QDRANT_COLLECTION_NAME,
    #                                             colour               = response["colour"],
    #                                             individual_category  = response["Individual_category"],
    #                                             category             = response["Category"],
    #                                             )

    # main_logger.info("Search completed successfully")
    # main_logger.info(f"Search results: {search_results}")
    # main_logger.info(f"Number of search results: {len(search_results)}")

if __name__ == "__main__":
    main()
