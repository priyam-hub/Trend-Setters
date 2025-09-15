# CUSTOM LLM BUILDER FOR EXTRACTOR AND PARSER

# DEPENDENCIES

import os
import sys
from peft import LoraConfig
from peft import get_peft_model
from transformers import pipeline
from langchain_groq import ChatGroq
from transformers import AutoTokenizer
from transformers import BitsAndBytesConfig
from transformers import AutoModelForCausalLM
from langchain_huggingface import HuggingFacePipeline

from logger.logger import LoggerSetup

# LOGGER SETUP
llm_builder_logger = LoggerSetup(logger_name = "llm_builder.py", log_filename_prefix = "llm_builder").get_logger()

# ------------------------------
# CHATGROQ LARGE LANGUAGE MODEL
#-------------------------------

def initialize_chatgroq_llm(temperature : float, groq_api_key : str, model_name : str) -> ChatGroq:
    """
    Initialize a ChatGroq LLM instance.

    Arguments:

        - `temperature`        {float}     : Sampling temperature for the LLM. Lower values make output deterministic, 
                                             higher values increase creativity.
        
        - `groq_api_key`        {str}      : API key for authenticating with Groq.
        
        - `model_name`          {str}      : The name of the LLM model to load.

    Returns
    
        - `llm`               {ChatGroq}   : An initialized ChatGroq LLM instance.

    Raises

        - `ValueError`                     : If initialization fails due to missing/invalid parameters or API issues.
    """
    try:
        
        if not groq_api_key:
            llm_builder_logger.error("Groq API key is missing.")
            
            raise ValueError("Groq API key is required.")
        
        if not model_name:
            llm_builder_logger.error("Model name is missing.")
            
            raise ValueError("Model name must be specified.")

        llm = ChatGroq(temperature   = temperature,
                       groq_api_key  = groq_api_key, 
                       model_name    = model_name
                       )

        llm_builder_logger.info(f"ChatGroq LLM initialized successfully with model: {model_name}")
        
        return llm

    except Exception as e:
        llm_builder_logger.error(f"Failed to initialize ChatGroq LLM: {repr(e)}")
        
        raise

# --------------------------------------------
# HUGGING-FACE FINE-TUNED LARGE LANGUAGE MODEL
#---------------------------------------------

# def initialize_hf_llm(hf_llm_model_name    : str, 
#                       max_new_tokens       : int = 512,
#                       temperature          : float = 0.5, 
#                       do_sample            : bool = True,
#                       use_lora             : bool = False,
#                       lora_r               : int = 8,
#                       lora_alpha           : int = 16,
#                       lora_dropout         : float = 0.05,
#                       lora_target_modules  : list = ["q_proj", "v_proj"]
#                       ) -> HuggingFacePipeline:
#     """
#     Initialize a Hugging Face LLM with 4-bit quantization and wrap it into a LangChain HuggingFacePipeline.

#     Arguments

#         - `hf_llm_model_name`              {str}                       : The Hugging Face model name or local path 
#                                                                          (e.g., "meta-llama/Llama-2-7b-chat-hf").
        
#         - `max_new_tokens`     {int, optional, default = 512}          : Maximum number of new tokens to generate.
        
#         - `temperature`       {float, optional, default = 0.5}         : Sampling temperature for text generation. 
#                                                                          Lower values = more deterministic, higher = more creative.
        
#         - `do_sample`         {bool, optional, default = True}         : Whether to use sampling; if False, uses greedy decoding.

#         - `use_lora`                {bool, default = False}            : Enable LoRA adapter injection if True.
        
#         - `lora_r`                     {int, default = 8}              : LoRA rank.
        
#         - `lora_alpha`                 {int, default = 16}             : LoRA scaling factor.
        
#         - `lora_dropout`            {float, default = 0.05}            : Dropout rate in LoRA layers.
        
#         - `lora_target_modules` {list, default = ["q_proj","v_proj"]}  : Target modules for LoRA injection.

#     Returns

#         - `llm`                     {HuggingFacePipeline}            : A LangChain-compatible Hugging Face pipeline object for 
#                                                                        text generation.

#     Raises

#         - `ValueError`                                               : If model name is missing or loading fails.
#     """
    
#     try:

#         if not hf_llm_model_name:
#             raise ValueError("Hugging Face model name must be provided.")

#         llm_builder_logger.info(f"Loading Hugging Face model: {hf_llm_model_name}")

#         # # QUANTIZATION CONFIGURATION FOR 4-BIT LOADING (FOR CUDA DEVICES)
#         # bnb_config    = BitsAndBytesConfig(load_in_4bit               = True,
#         #                                    bnb_4bit_use_double_quant  = True,
#         #                                    bnb_4bit_quant_type        = "nf4",
#         #                                    bnb_4bit_compute_dtype     = "bfloat16"
#         #                                    )

#         # llm_builder_logger.info("Quantization configuration set for 4-bit loading")

#         # LOADING MODEL AND TOKENIZER
#         tokenizer     = AutoTokenizer.from_pretrained(hf_llm_model_name)
        
#         model         = AutoModelForCausalLM.from_pretrained(hf_llm_model_name, 
#                                                              device_map           = "auto"
#                                                              )

#         llm_builder_logger.info("Model and tokenizer loaded successfully")

#         # APPLY LORA CONFIG IF ENABLED
#         if use_lora:
#             llm_builder_logger.info("Applying LoRA configuration...")
            
#             lora_config = LoraConfig(r                = lora_r,
#                                      lora_alpha       = lora_alpha, 
#                                      target_modules   = lora_target_modules, 
#                                      lora_dropout     = lora_dropout, 
#                                      bias             = "none", 
#                                      task_type        = "CAUSAL_LM"
#                                      )
            
#             model       = get_peft_model(model, lora_config)
            
#             llm_builder_logger.info(f"LoRA applied with r = {lora_r}, alpha = {lora_alpha}, dropout = {lora_dropout}")

#         else:
#             llm_builder_logger.info("LoRA not enabled, using base model only.")

#         # BUILDING THE TEXT GENERATION PIPELINE
#         pipe          = pipeline("text-generation",
#                                  model           = model, 
#                                  tokenizer       = tokenizer, 
#                                  max_new_tokens  = max_new_tokens, 
#                                  temperature     = temperature, 
#                                  do_sample       = do_sample
#                                  )

#         llm_builder_logger.info("Text generation pipeline created successfully")

#         llm           = HuggingFacePipeline(pipeline = pipe)

#         llm_builder_logger.info(f"Hugging Face LLM initialized successfully with model: {hf_llm_model_name}")
        
#         return llm

#     except Exception as e:
#         llm_builder_logger.error(f"Failed to initialize Hugging Face LLM: {str(e)}")
        
#         raise