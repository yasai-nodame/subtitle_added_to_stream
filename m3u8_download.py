import asyncio 
import aiohttp 
import m3u8
import os
import aiofiles
from moviepy.editor import VideoFileClip
import time

import write_subtitle_text
import video_path
import file_remove 


#############################################################
# ライブ配信が取得できてるかチェックする response.status=200
#############################################################
async def response_valid(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status


##########################################################
# ライブ配信のm3u8ファイルを取得し、tsファイルを取得していく
##########################################################  # これが非同期で常に実行してるので、ファイル削除をするときにプロセス使用中とでる。　同期処理にしたらどうなるか。
async def download_ts_segments(playlist_url, output_dir, count, m3u8_files):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(playlist_url) as response:
                playlist = m3u8.loads(await response.text())
                for segment in playlist.segments:
                    ts_url = segment.uri
                    if not ts_url in m3u8_files:
                        ts_filename = f'file{count}.ts'
                        output_path = os.path.join(output_dir, ts_filename)
                        async with session.get(ts_url) as ts_response:
                            async with aiofiles.open(output_path, mode='wb') as f:
                                await f.write(await ts_response.read())
                                print(f'Downloaded: {ts_url}')
                            count += 1
                            m3u8_files.append(ts_url)
                            
            return count
    except Exception as e:
        print('エラーが発生しました。', e)

###################################################
# 取得したtsファイルから音声だけを切り出して取得する
###################################################
async def extract_audio_async(video_file, audio_file):
    # tsファイルから音声を抽出して保存する
    clip = VideoFileClip(video_file)
    audio_clip = clip.audio
    audio_clip.write_audiofile(audio_file)


async def main():
    url = video_path.os.environ.get('TWICH_URL')
    count = 0 
    i = 0
    lock = asyncio.Lock()
    
    subtitle_srt = os.path.join(video_path.os.environ.get('SRT_DIRECTORY'), f'subtitle{i}.srt')
    
    output_dir = video_path.os.environ.get('VIDEO_FILE_PATH')
    files_name = []
    while True:
        video_file = os.path.join(video_path.os.environ.get('VIDEO_FILE_PATH'), f'file{i}.ts')
        audio_file = os.path.join(video_path.os.environ.get('AUDIO_FILE_PATH'), f'output_audio{i}.wav')
        status_valid = await response_valid(url)
        count = await download_ts_segments(url, output_dir, count, files_name)
        
        try:
            if i > 100:
                async with lock:
                    await file_remove.ts_remove(i - 101)
        except Exception as e:
            time.sleep(1)
            print('エラーです' , e)
        
        # 動画ファイルが存在しなかったらpass、存在したら音声抽出する
        if not os.path.exists(video_file):
            continue
        else:
            # ビデオと音声を切り離す
            await extract_audio_async(video_file, audio_file)
            
            # 音声ファイルからテキスト抽出、ビデオファイルから時間抽出、srtファイル生成
            await write_subtitle_text.extracted_from_audio(audio_file, video_file, i)
            
            # ビデオ、音声、字幕の複数のメディアストリームをmkvファイルに変換
            if subtitle_srt is None:
                subtitle_srt = None
                await write_subtitle_text.transform_mkv(video_file, audio_file, subtitle_srt, i)
            else:
                await write_subtitle_text.transform_mkv(video_file, audio_file, subtitle_srt, i)
        
        
        # ライブ配信が終わったらbreakする
        if status_valid != 200:
            print('ライブ配信が終わったので、終了します。')
            time.sleep(5)
            break 
        
        i += 1
        
if __name__ == '__main__':
    asyncio.run(main())
