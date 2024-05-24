import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks
import srt
from datetime import timedelta


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')


def recognize_speech_from_audio(audio_path, chunk_length_ms=7000):
    audio = AudioSegment.from_wav(audio_path)
    chunks = make_chunks(audio, chunk_length_ms)

    recognizer = sr.Recognizer()
    subtitles = []

    for i, chunk in enumerate(chunks):
        chunk_name = f"chunk{i}.wav"
        chunk.export(chunk_name, format="wav")
        with sr.AudioFile(chunk_name) as source:
            audio_listened = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_listened, language="ru-RU")
                start_time = timedelta(milliseconds=i * chunk_length_ms)
                end_time = start_time + timedelta(milliseconds=chunk_length_ms)
                subtitle = srt.Subtitle(index=i, start=start_time, end=end_time, content=text)
                subtitles.append(subtitle)
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                continue

    return subtitles


def create_srt_file(subtitles, srt_path):
    srt_content = srt.compose(subtitles)
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)


video_path = "video.mp4"
audio_path = "extracted_audio.wav"
srt_path = "subtitler/horizontal/subtitles.srt"

if __name__ == "__main__":
    extract_audio_from_video(video_path, audio_path)
    subtitles = recognize_speech_from_audio(audio_path)
    create_srt_file(subtitles, srt_path)
