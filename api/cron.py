import logging
logger = logging.getLogger(__name__)
from api.views import youTubeApi
from api.models import VideoDetail

def callAPI():
    logger.info("API Call is initiated")     #logging
    youTubeApi()                             #calling youtube api from api.views
    logger.info("API Call is completed")

def deleteCache():
    VideoDetail.objects.all().delete()       # deleting data to prevent database from overflow as we are using lite database
    logger.info("Cache Cleared")
