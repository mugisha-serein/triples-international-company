from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def global_exception_handler(exc, context):
    """
    Standardizes API errors and hides sensitive details in production.
    """
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Personalize standard DRF errors if needed
        if isinstance(response.data, dict):
            response.data['status_code'] = response.status_code
        elif isinstance(response.data, list):
            response.data = {'detail': response.data, 'status_code': response.status_code}
    else:
        # Handle unhandled exceptions (e.g. 500 errors)
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        
        response = Response({
            'detail': 'A server error occurred. Please contact support.',
            'status_code': 500
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
