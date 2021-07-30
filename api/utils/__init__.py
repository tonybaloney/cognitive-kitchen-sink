from functools import wraps
import logging
import os
import azure.functions as func


def debuggable(default=False):
    def debuggable_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                if os.getenv('DEBUG', default):
                    logging.exception(exc)
                    import sys, traceback
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    exception_details = traceback.format_exception(exc_type, exc_value,
                                                    exc_traceback)
                    response = '<html><body><h1>Server Error</h1>'
                    for t in exception_details:
                        response += '<pre>' + t + '</pre>'
                    response += '</body></html>'
                    return func.HttpResponse(
                        response,
                        mimetype="text/html",
                        status_code=500
                    )
                else:
                    return func.HttpResponse(
                        "Unhandled Server Error, set DEBUG to True to see the exception details.",
                        status_code=500
                    )
        return wrapper
    return debuggable_decorator
