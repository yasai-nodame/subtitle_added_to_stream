import speech_recognition as sr
import os
import ffmpeg

import video_duration
import video_path

###############################
# 音声からsrtファイルを作成する
###############################
async def extracted_from_audio(audio_file, video_file, count):
    subtitle_file = os.path.join(video_path.os.environ.get('SRT_DIRECTORY'), f'subtitle{count}.srt')
    
    try:
        r = sr.Recognizer()
        
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)

        text = r.recognize_google(audio_data, language='ja-JP')

        # 字幕をテキストファイルに随時追加していく
        with open(subtitle_file, 'w', encoding='utf-8') as f:
            f.write(f'{count + 1}\n')
            f.write(f'{await video_duration.first_format(video_duration.get_video_duration(video_file))}\n')
            f.write(text + '\n')
            
    except Exception as e:
        print(f'Error: {e}')
        pass


#################################################################################################################
# 動画、音声、字幕等の複数のメディアストリームを格納できるmkv拡張子に変換する こうすることでライブ配信に字幕がつけれる
#################################################################################################################
async def transform_mkv(video, audio, subtitle, count):
    input_video = ffmpeg.input(video)
    input_audio = ffmpeg.input(audio)
    
    if not os.path.exists(subtitle):
        output = (
        ffmpeg.output(input_video['v'], input_audio['a'], os.path.join(video_path.os.environ.get('MKV_DIRECTORY'), f'output{count}.mkv'), c='copy')
    )
        
    else:
        input_subtitle = ffmpeg.input(subtitle)
        output = (
            ffmpeg.output(input_video['v'], input_audio['a'], input_subtitle['s'], os.path.join(video_path.os.environ.get('MKV_DIRECTORY'), f'output{count}.mkv'), c='copy')
        )
    
    ffmpeg.run(output)


