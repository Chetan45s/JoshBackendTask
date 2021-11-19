import logging
from django_filters.rest_framework import DjangoFilterBackend
from httplib2 import Response
from rest_framework import generics,filters
from api.models import VideoDetail
from api.serializers import VideoDetailSerializer
from rest_framework.pagination import PageNumberPagination
from apiclient.errors import HttpError

from backendTaskFetchYoutubeApi import settings
import googleapiclient.discovery
import googleapiclient.errors
import datetime


# spliting date from R338 format to search for post using publishedAfter query provied by user
def getDate(date):
    splited_date = date.split("-")
    year,month,day = splited_date[0],splited_date[1],splited_date[2][slice(2)]
    return int(year),int(month),int(day)


# API logic to serialize data 

# we added couple of things as mentioned after publisedAfter query so 
# if publisedAfter query is not provided then we are rendering cached data and if provided
# we are filtering database for results published after that partcular date
class FetchAPI(generics.ListAPIView):
    serializer_class = VideoDetailSerializer

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)

    search_fields = ['videoTitle','description']  # Searching on videoTitle and Descriptiion

    ordering = ['-publishingDatetime',]           # Default sorted on publishingDateTime
    pagination_class = PageNumberPagination       # Using default pagination defined in settings.py

    def get_queryset(self):
        publishedAfter = self.request.query_params.get('publishedAfter')  # getting query from user
        if publishedAfter is None:                                        # checking where data is given or not
            return VideoDetail.objects.all()                              # if not given then returning cached result
        else:                                                             # else applying the filter
            print(publishedAfter)
            year,month,day = getDate(publishedAfter)
            return VideoDetail.objects.filter(publishingDatetime__gt=datetime.date(year,month,day))


# function to call youtube API this function is called in the interval of 2 minutes

def youTubeApi():

    api_service_name = "youtube"
    api_version = "v3"
    api_keys = settings.API_KEYS  # getting kets from settings.py
    api_response = False

    for key in api_keys:  # trying to use all apikeys from the list if in case one doesn't work or fail

        try:
            youtube = googleapiclient.discovery.build(             
            api_service_name, api_version, developerKey=key)      #calling youtube api

            request = youtube.search().list(
                part="snippet",
                maxResults=20,
                order="date",
                q="cricket"                
            )           # for query we are using cricket keyword, and maximum result in each request is 20
            response = request.execute() 
            api_response = True        # if api execute successfully then setting api_response  = True to stop the loop
            

        except HttpError as er:       # basic error handling
            err_code = er.resp.status
            if not(err_code == 400 or err_code == 403):
                logging.info("Some Error Occured plase check API KEY validity")
                break

        if api_response:
            logging.info("API Executed")    # logging
            break
        
    if api_response: # extraction information from the json and storing the result in the database
        for obj in response['items']:
            videoTitle = obj['snippet']['title']
            description = obj['snippet']['description']
            publishingDatetime = obj['snippet']['publishedAt']
            thumbnailURL = obj['snippet']['thumbnails']['default']['url']

            VideoDetail.objects.create(
                videoTitle=videoTitle, 
                description=description,
                publishingDatetime=publishingDatetime, 
                thumbnailURL=thumbnailURL,
            )
