import time 
import vlc
import os 
import re
from itertools import zip_longest
import asyncio

import video_path
import file_remove

###########################################
# VLCで、ライブ配信のファイルを再生し続ける
###########################################
async def play_mkv_files(mkv_directory, srt_directory, lock):
    # VLC インスタンス化
    instance = vlc.Instance('--sub-source=marq')
    player = instance.media_player_new()
    
    playing_mkv_files = set()
    playing_srt_files = set()
    while True:
        # ディレクトリ内の mkv ファイル,srtファイルを順番に再生
        mkv_files = set(f for f in os.listdir(mkv_directory) if f.endswith('.mkv'))
        srt_files = set(f for f in os.listdir(srt_directory) if f.endswith('.srt'))
        
        # 新しいmkvファイル,srtファイルが追加された場合に、再生リストに追加
        new_mkv_files = mkv_files - playing_mkv_files
        new_srt_files = srt_files - playing_srt_files
        
        # set()によって要素がバラバラになってるのでsorted()で整形する。 それだけだと1,10,2の順番になるので key=lambdaを使って最初の数字の部分を抽出しint()にいれ、group()で部分文字列を取得。
        sort_mkv_files = sorted(new_mkv_files, key=lambda x: int(re.search(r'\d+', x).group()))
        sort_srt_files = sorted(new_srt_files, key=lambda x: int(re.search(r'\d+', x).group()))
        

        
        for mkv_file,srt_file in zip_longest(sort_mkv_files, sort_srt_files):
            if srt_file is None:
                mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                
                mkv_file_path = os.path.join(mkv_directory, mkv_file)
                
                if len(os.listdir(mkv_directory)[:-10]) < mkv_file_number:
                    print('ファイルに追いつくので、100秒遅延を発生させます。')
                    time.sleep(100)
                
                media = instance.media_new(mkv_file_path)
                player.set_media(media)
                
                if player.play() == -1:
                    print(f'ファイルが破損していました。: {mkv_file_path}')
                    time.sleep(3)
                    continue
                
                playing_mkv_files.add(mkv_file)
            
                start_time = time.time()
                while player.get_state() not in (vlc.State.Playing, vlc.State.Error, vlc.State.Ended):
                    if time.time() - start_time > 2:
                        print(f'再生が開始されませんでした。: {mkv_file_path}')
                        player.stop()
                        break 
                    time.sleep(0.1)
                
                if player.get_state() in (vlc.State.Error, vlc.State.Ended):
                    print(f'再生中にエラーが発生しました。: {mkv_file_path}')
                    time.sleep(3)
                    continue 
                
                if player.get_state() == vlc.State.playing:
                    duration = player.get_length() / 1000
                    time.sleep(duration)
                
                if mkv_file_number > 50:
                    async with lock:
                        await file_remove.file_remove(mkv_file_number - 51)
            else:
                mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                srt_file_number = int(re.search(r'\d+', srt_file).group())
            
                if mkv_file_number == srt_file_number:
                    mkv_file_path = os.path.join(mkv_directory, mkv_file)
                    srt_file_path = os.path.join(srt_directory, srt_file)
                    
                    mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                    
                    if len(os.listdir(mkv_directory)[:-10]) < mkv_file_number:
                        print('ファイルに追いつくので、100秒遅延を発生させます。')
                        time.sleep(100)
                    
                    # mkv ファイルを再生
                    media = instance.media_new(mkv_file_path)
                    media.add_option(f':sub-file={srt_file_path}')
                    player.set_media(media)
                    
                    if player.play() == -1:
                        print(f'ファイルが破損していました。: {mkv_file_path}')
                        time.sleep(3)
                        continue 
                    
                    playing_mkv_files.add(mkv_file)
                    playing_srt_files.add(srt_file)
                    
                    start_time = time.time()
                    while player.get_state() not in (vlc.State.Playing, vlc.State.Error, vlc.State.Ended): 
                        if time.time() - start_time > 2:
                            print(f'再生が開始されませんでした。: {mkv_file_path}')
                            player.stop()
                            break 
                        time.sleep(0.1)
                    
                    if player.get_state() in (vlc.State.Error, vlc.State.Ended):
                        print(f'再生中にエラーが発生しました。: {mkv_file_path}')
                        time.sleep(3)
                        continue 
                    
                    
                    if player.get_state() == vlc.State.Playing:
                        # 再生が終了するまで待機
                        duration = player.get_length() / 1000
                        time.sleep(duration)
                    
                    if mkv_file_number > 50:
                        async with lock:
                            await file_remove.file_remove(mkv_file_number - 51)
                        
                elif mkv_file_number != srt_file_number:
                        mkv_file_path = os.path.join(mkv_directory, mkv_file)
                        
                        mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                        
                        if len(os.listdir(mkv_directory)[:-10]) < mkv_file_number:
                            print('ファイルに追いつくので、100秒遅延を発生させます。')
                            time.sleep(100)
                            
                        media = instance.media_new(mkv_file_path)
                        player.set_media(media)
                        
                        if player.play() == -1:
                            print(f'ファイルが破損していました。: {mkv_file_path}')
                            time.sleep(3)
                            continue 
                        
                            
                        playing_mkv_files.add(mkv_file)
                        
                        start_time = time.time()
                        while player.get_state() not in (vlc.State.Playing, vlc.State.Error, vlc.State.Ended):
                            if time.time() - start_time > 2:
                                print(f'再生が開始されませんでした。: {mkv_file_path}')
                                player.stop()
                                break
                            time.sleep(0.1)
                        
                        if player.get_state() in (vlc.State.Error, vlc.State.Ended):
                            print(f'再生中にエラーが発生しました。: {mkv_file_path}')
                            time.sleep(3)
                            continue
                        
                        if player.get_state() == vlc.State.Playing:
                            duration = player.get_length() / 1000
                            time.sleep(duration)
                        
                        if mkv_file_number > 50:
                            async with lock:
                                await file_remove.file_remove(mkv_file_number - 51)
            
            # 再生が終了したファイルを再生リストから削除
            for mkv_file, srt_file in zip(playing_mkv_files.copy(), playing_srt_files.copy()):
                if not os.path.exists(os.path.join(mkv_directory, mkv_file)):
                    playing_mkv_files.remove(mkv_file)
                if not os.path.exists(os.path.join(srt_directory, srt_file)):
                    playing_srt_files.remove(srt_file)
            
            break
        

async def main():
    mkv_file = video_path.os.environ.get('MKV_DIRECTORY')
    srt_file = video_path.os.environ.get('SRT_DIRECTORY')
    lock = asyncio.Lock()
    
    print('約100秒後に、ライブを再生します。')
    while True:
        if len(os.listdir(mkv_file)) > 100:
            await play_mkv_files(mkv_file, srt_file, lock)
        else:
            continue
        
        
if __name__ == '__main__':
    asyncio.run(main())
