import random,os,vk_api,pyshorteners,urllib.request,feedparser
from deep_translator import GoogleTranslator
from vk_api import VkUpload
from random import randrange
from GoogleNews import GoogleNews
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from bing_image_urls import bing_image_urls
a=["-67860517","-76456136"]
zapros=random.choice(a)
try:
  rand=randrange(100)
  posts = vk.wall.get(owner_id=zapros, count=100)['items']
  text = [post['text'] for post in posts]
  id = [post['id'] for post in posts]
except:
  pass
try:
  parser = 'html.parser'
  resp = urllib.request.urlopen("https://vk.com/wall"+str(zapros)+"_"+str(id[rand]))
  soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
  for link in soup.find_all('a', href=True):
     if link['href'].startswith("/video-"):
        stripped = link['href'].split("?", 1)[0]
except:
  pass
try:
  response = vk.wall.post(owner_id="-106906481",from_group=1,message=text[rand],attachments=stripped.replace("/",""))
except:
  pass
