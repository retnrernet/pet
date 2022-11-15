import streamlit as st
import os, ffmpeg, subprocess,glob,re,datetime
import time as tm
from multiprocessing import Process
from time import sleep
from infomedia import mediainfo
from datetime import time
from moviepy.video.io.VideoFileClip import VideoFileClip,AudioFileClip
from pathlib import Path
filename = st.sidebar.text_input('Введи имя файла:') or st.sidebar.file_uploader("Выбери файл")
pre=st.sidebar.checkbox("Проксировать", value=False)
if filename:
  if pre:
    ffmpeg_command = ["ffmpeg", "-y", "-i", filename, "-s", "90x50","-crf","3","-preset","ultrafast","output.mp4"]
    pipe = subprocess.run(ffmpeg_command, threaded=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  else:
    ffmpeg_command = ["ffmpeg", "-y", "-i", filename, "-c", "copy", "-an","output.mp4"]
    pipe = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  video_file = open("output.mp4", 'rb')
  video_bytes = video_file.read()
  st.sidebar.video(video_bytes)
  data = mediainfo(filename)
  values = st.slider('Таймлайн',0.0, data['format']['duration'], (0.0, data['format']['duration']))
  if values:
    start=str(values).replace("(","").replace(")","").split(",")[0]
    end=str(values).replace("(","").replace(")","").split(", ")[1]
    sm=datetime.timedelta(seconds=round(float(start)))
    em=datetime.timedelta(seconds=round(float(end)))
    st.code(str(sm)+", "+str(em))
  col1, col2, col3 = st.columns([1,1,1])
  with col1:
    adjust=st.checkbox("Компрессия аудио", value=False)
    brightness=st.checkbox("Яркость", value=False)
    tr1=st.checkbox("Fadein", value=False)
    tr2=st.checkbox("Fadeout", value=False)
  with col2:
    if st.button("Оставить клип в рамках"):
      start=str(values).replace("(","").replace(")","").split(",")[0]
      end=str(values).replace("(","").replace(")","").split(", ")[1]
      my_file = Path("end1.mp4")
      if my_file.is_file():
        list_of_files = glob.glob('/content/end*.mp4')
        latest_file = max(list_of_files, key=os.path.getctime)
        num=re.findall(r'\d+', latest_file.replace(".mp4",""))
        num1=int(str(num).replace("['","").replace("']",""))+1
        name=latest_file.replace(str(num).replace("['","").replace("']",""),str(num1))
      else:
        name="end1.mp4"
      ffmpeg_command = ["ffmpeg", "-y", "-i", filename,"-ss", start,"-t",end, "-c:v", "copy", name]
      pipe = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      if adjust:
        import moviepy.audio.fx.all as afx
        videoclip = VideoFileClip(name).fx(afx.audio_normalize)
        videoclip.write_videofile(name, audio_codec='aac')
      if brightness:
        import moviepy.video.fx.all as vfx
        videoclip = VideoFileClip(name).fx(vfx.colorx, 1.2)
        videoclip.write_videofile(name, audio_codec='aac')
      if tr1:
        import moviepy.video.fx.all as vfx
        videoclip = VideoFileClip(name).fx(vfx.fadein, 1.0)
        videoclip.write_videofile(name, audio_codec='aac')
      if tr2:
        import moviepy.video.fx.all as vfx
        videoclip = VideoFileClip(name).fx(vfx.fadeout, 1.0)
        videoclip.write_videofile(name, audio_codec='aac')
      video_file = open(name, 'rb')
      video_bytes = video_file.read()
      st.sidebar.video(video_bytes)
  with col3:
    if st.button("Рендер"):
      f_data = 'file \'' + '\'\nfile \''.join(glob.glob('/content/end*.mp4')) + '\''
      f_list = 'mylist.txt'
      with open(f_list, 'w', encoding='gbk') as f:
        f.write(f_data)
      new = []
      with open ("mylist.txt","r") as f:
        for line in f:
          stripped = line.strip("\n")
          new.append(stripped)
      new.sort()
      with open ("mylist.txt","w") as file:
        for k in new:
          file.write(k + "\n")
      #raw = ["ffmpeg", "-y", "-map", "0:v", "-c:v", "copy", "-f", "concat", "-safe","0","-i","mylist.txt","-bsf:v","h264_mp4toannexb", "raw.h264"]
      ffmpeg_command = ["ffmpeg", "-y", "-f", "concat", "-i", "mylist.txt", "-c:v", "copy", "out.mp4"]
      #pipe = subprocess.run(raw, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      pipe = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      with open("out.mp4", "rb") as file:
        btn = st.download_button(label="Скачать",data=file,file_name="out.mp4", mime="video/mp4")
