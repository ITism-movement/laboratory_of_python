from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import srt
from textwrap import wrap


def parse_srt(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f:
        subtitles = list(srt.parse(f.read()))
    return subtitles


def add_animated_subtitles(video_path, srt_path, output_path, font_path, font_size=24, color='white', bg_color='blue',
                           max_chars=20, y_offset=50, fade_duration=0.5):
    video = VideoFileClip(video_path)
    subtitles = parse_srt(srt_path)

    def make_text_clip(subtitle):
        start = subtitle.start.total_seconds()
        end = subtitle.end.total_seconds()
        wrapped_text = "\n".join(wrap(subtitle.content, width=max_chars))  # Automatically wrap text
        txt_clip = TextClip(wrapped_text, fontsize=font_size, font=font_path, color=color, bg_color=bg_color,
                            stroke_color=None, stroke_width=0, align='center', size=(video.w * 0.9, None))
        txt_clip = txt_clip.set_position(('center', video.h - y_offset - txt_clip.h)).set_start(start).set_end(end)
        txt_clip = txt_clip.crossfadein(fade_duration).crossfadeout(fade_duration)
        return txt_clip

    text_clips = [make_text_clip(subtitle) for subtitle in subtitles]
    final_clip = CompositeVideoClip([video] + text_clips)
    final_clip = final_clip.set_audio(video.audio)  # Ensure audio is included
    final_clip.write_videofile(output_path, codec="libx264", audio_codec='aac')


video_path = "video_2.mp4"
srt_path = "split_subtitles.srt"
font_path = "robo-font/RobotoMono-Regular.ttf"  # Укажите путь к файлу шрифта
output_path = "vertical_video_with_animated_subtitles.mp4"
add_animated_subtitles(video_path, srt_path, output_path, font_path, font_size=24, color='white', bg_color='blue',
                       max_chars=20, y_offset=100, fade_duration=0.5)
