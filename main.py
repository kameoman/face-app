import streamlit as st
import io
import requests
import json
from PIL import Image, ImageDraw, ImageFont


st.title('顔認識アプリ')

subscription_key = st.secrets["SUBSCRIPTION_KEY"]
assert subscription_key

face_api_url = 'https://20210813spiderkame.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
  img = Image.open(uploaded_file)
  with io.BytesIO() as output:
      img.save(output, format="JPEG")
      binary_img = output.getvalue()
  headers = {
      'Content-Type': 'application/octet-stream',
      'Ocp-Apim-Subscription-Key': subscription_key
  }
  params = {
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'false',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
  }

  res= requests.post(face_api_url, params=params, headers=headers, data=binary_img)
  results = res.json()

  for result in results:
    #   at_rect = result['faceRectangle']
    
      at_rect = result['faceAttributes']
      gender = at_rect['gender']
      age = at_rect['age']
      smile = at_rect['smile']
      font = ImageFont.truetype('NikkyouSans-mLKax.ttf', 15)
        
      draw = ImageDraw.Draw(img)
      draw.rectangle([(at_rect['left'], at_rect['top']), (at_rect['left']+at_rect['width'],at_rect['top']+at_rect['height'])], fill=None, outline='green', width=5)
      draw.text((70+at_rect['left'], 10+at_rect['top']+at_rect['height']),gender, font=font,fill='#008000')
      draw.text((at_rect['left'], 10+at_rect['top']+at_rect['height']),'gender:', font=font,fill='#008000')
      draw.text((60+at_rect['left'], 25+at_rect['top']+at_rect['height']),str(age), font=font,fill='#008000')
      draw.text((at_rect['left'], 25+at_rect['top']+at_rect['height']),'age:', font=font,fill='#008000')
      draw.text((at_rect['left'], 40+at_rect['top']+at_rect['height']),'smile:', font=font,fill='#008000')
      draw.text((60+at_rect['left'], 40+at_rect['top']+at_rect['height']),str(smile), font=font,fill='#008000')

  st.image(img, caption='Uploaded Image.', use_column_width=True)