import contextvars
import hashlib
import json
import logging
from logging.handles import RotatingFileHandler
import sys
import uuid

from langchain_core,callbacks import BaseCallbackHandler
from langchain_core.output_parsers import StrOutParser 
from langchain_core.prmpts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from rag_indexer imprt cargar_vectorstore, formatear_contexto