import datetime
from moviepy.editor import VideoFileClip

async def first_format(duration):
    def init_format():
        # 初期の開始時間と終了時間
        initial_start_time = datetime.datetime.strptime("00:00:00,000", "%H:%M:%S,%f")
        initial_end_time = datetime.datetime.strptime("00:00:00,000", "%H:%M:%S,%f")

        added_time = datetime.timedelta(seconds=duration)

        # 新しい開始時間と終了時間
        new_start_time = initial_start_time 
        new_end_time = initial_end_time + added_time

        # フォーマットされた文字列に変換
        formatted_start_time = new_start_time.strftime("%H:%M:%S,%f")[:-3]  # マイクロ秒以下の小数点以下3桁を削除
        formatted_end_time = new_end_time.strftime("%H:%M:%S,%f")[:-3]  # マイクロ秒以下の小数点以下3桁を削除

        # フォーマットされた文字列の出力
        formatted_string = "{} --> {}".format(formatted_start_time, formatted_end_time)
        format_list.append(formatted_end_time)
        
        return formatted_string
    formatted_string = init_format()
    return formatted_string

def get_video_duration(video_file):
    clip = VideoFileClip(video_file)
    duration = clip.duration 
    clip.close() 
    return duration 

format_list = []



