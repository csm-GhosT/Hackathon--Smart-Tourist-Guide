import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import json
import wikipedia
from gtts import gTTS
from google.auth._default import _load_credentials_from_file
class VisionAi():
    wiki_link =''
    summary=''
    title=''

    def set_title(self,name):
        self.title=name

    def get_title(self):
        return self.title

    def set_summary(self,summary):
        self.summary =summary

    def set_wiki_link(self,link):
        self.wiki_link =link

    def get_summary(self):
        return self.summary

    def get_wiki_link(self):
        return self.wiki_link



    def search_vision(self,impath):
        client=vision.ImageAnnotatorClient()
        try:
            with io.open(impath,'rb') as image_file:
                content = image_file.read()
        except:
            return 'no_img_found'

        image = vision.types.Image(content=content)

        response = client.landmark_detection(image=image)
        # print(response)

        landmarks= response.landmark_annotations


        df = pd.DataFrame(columns=[ 'description','locations','score'])
        # check if df is empty i.e no responce from Vision

        for landmark in landmarks:
            df = df.append(
                dict(
                    description=landmark.description,
                    location=landmark.locations,
                    score=landmark.score

                ),
                ignore_index=True
            )

        if(df.empty):
            return 'search_not_found'


        print(df['description'][0])
        # ny =
        self.set_summary(wikipedia.summary(df['description'][0]))
        self.set_wiki_link(wikipedia.page(df['description'][0]).url)
        self.set_title(str(df['description'][0]))

        return (self.get_summary())
