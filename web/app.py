# FLASK SERVER

# DEPENDENCIES

import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from huggingface_hub import login
from qdrant_client import QdrantClient

from src.parser.parser import parser
from src.extractor.extractor import extractor
# from src.llm.llm_builder import initialize_hf_llm
from src.searcher.searcher import search_collection
from src.llm.llm_builder import initialize_chatgroq_llm

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
app_logger                 = LoggerSetup(logger_name = "app.py", log_filename_prefix = "app").get_logger()

app                        = Flask(__name__, static_folder = 'static', template_folder = 'templates')

# RENDERING THE HOME PAGE
@app.route('/')
def home():
    return render_template('index_home.html')

# RENDERING THE CHATBOT PAGE
@app.route('/chatbot')
def chatbot():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():

    try:

        # Get the query from the request
        data                    = request.json
        conversation_history    = data.get('query', '')

        # INITIALIZING THE QDRANT CLIENT
        client                  = QdrantClient(url      = QDRANT_CLUSTER_URL, 
                                               api_key  = QDRANT_API_KEY
                                               )

        app_logger.info("Qdrant client initialized successfully")

        app_logger.info(f"GROQ_API_KEY : {'Present' if GROQ_API_KEY else 'Not Present'}")
        app_logger.info(f"LLM_MODEL_NAME : {LLM_MODEL_NAME if LLM_MODEL_NAME else 'Not Present'}")

        # INITIALIZING THE CHATGROQ LLM
        llm                     = initialize_chatgroq_llm(temperature   = 0.5, 
                                                          groq_api_key  = GROQ_API_KEY, 
                                                          model_name    = LLM_MODEL_NAME
                                                          )
        
        app_logger.info("ChatGroq LLM initialized successfully")

        # login(HUGGINGFACE_LOGIN_TOKEN)

        # app_logger.info(f"HuggingFace login successful: {'Yes' if HUGGINGFACE_LOGIN_TOKEN else 'No'}")

        # # INITIALIZING THE HUGGING FACE LARGE LANGUGAGE MODEL
        # llm                     = initialize_hf_llm(hf_llm_model_name   = HF_LLM_MODEL_NAME, 
        #                                             temperature         = 0.5, 
        #                                             max_new_tokens      = 512, 
        #                                             do_sample           = True,
        #                                             use_lora            = True,
        #                                             lora_r              = 8,
        #                                             lora_alpha          = 16,
        #                                             lora_dropout        = 0.05,
        #                                             lora_target_modules = ["q_proj", "v_proj"]
        #                                             )

        # app_logger.info("Fine-Tuned LLM initialized successfully")

        extractor_response      = extractor(llm                   = llm, 
                                            conversation_history  = conversation_history
                                            )

        app_logger.info(f"Extractor response: {extractor_response}")

        response                = parser(response = extractor_response)

        if response["MOVE_ON"]:

            search_results      = search_collection(client               = client, 
                                                    collection_name      = QDRANT_COLLECTION_NAME, 
                                                    colour               = response["colour"], 
                                                    individual_category  = response["Individual_category"], 
                                                    category             = response["Category"],
                                                    )
            app_logger.info("Search completed successfully")
            app_logger.info(f"Search results: {len(search_results)}")

            return jsonify({"results": search_results, "message": "Search results for your query"})
        
        else:
            app_logger.info("Insufficient information to perform search")
            
            return jsonify({"results": [], "message": response["FOLLOW_UP_MESSAGE"]})

    except Exception as e:

        return jsonify({"error": repr(e)}), 500



if __name__ == '__main__':
    app.run(debug = True)