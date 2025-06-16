from phoenix.trace.openai import instrument_openai
import os

phoenix_server = os.getenv("PHOENIX_HOST", "http://phoenix:6006")
instrument_openai(server_url=phoenix_server)
