"""Entry point for Google Cloud Functions (2nd gen) deploy.

The framework looks for main.py at the project root and the entry point
function (cloud_function_handler). We re-export from api.main so that
the same code runs locally via uvicorn (api.main:app) and on GCF.
"""

from api.main import cloud_function_handler

__all__ = ["cloud_function_handler"]
