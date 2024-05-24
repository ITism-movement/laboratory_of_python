import srt
from datetime import timedelta

from add_subtitles_to_video import add_subtitles_to_video
from make_subtitles import create_srt_file, video_path, srt_path

import srt
from datetime import timedelta


def split_long_subtitles(subtitles, max_duration_ms=3500):
    new_subtitles = []
    subtitle_index = 1  # Индекс для новых субтитров

    for subtitle in subtitles:
        words = subtitle.content.split()
        num_words = len(words)
        num_chunks = max(1, int((subtitle.end - subtitle.start).total_seconds() * 1000 // max_duration_ms))
        words_per_chunk = max(1, num_words // num_chunks)

        for i in range(num_chunks):
            start_time = subtitle.start + timedelta(milliseconds=i * max_duration_ms)
            end_time = min(subtitle.start + timedelta(milliseconds=(i + 1) * max_duration_ms), subtitle.end)
            chunk_content = ' '.join(words[i * words_per_chunk:(i + 1) * words_per_chunk])
            new_subtitle = srt.Subtitle(index=subtitle_index, start=start_time, end=end_time, content=chunk_content)
            new_subtitles.append(new_subtitle)
            subtitle_index += 1

    return new_subtitles


# Загрузим существующий файл субтитров
with open(srt_path, "r", encoding="utf-8") as f:
    subtitles = list(srt.parse(f.read()))

# Разделим длинные строки субтитров
split_subtitles = split_long_subtitles(subtitles)

# Создадим новый файл субтитров с разделенными строками
new_srt_path = "subtitler/horizontal/split_subtitles.srt"
create_srt_file(split_subtitles, new_srt_path)

# Добавим новые субтитры к видео
output_video_path = "video_with_split_subtitles.mp4"
add_subtitles_to_video(video_path, new_srt_path, output_video_path)
