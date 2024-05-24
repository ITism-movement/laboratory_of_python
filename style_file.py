import srt


def timedelta_to_ass_time(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    centiseconds = td.microseconds // 10000
    return f"{hours}:{minutes:02}:{seconds:02}.{centiseconds:02}"


def create_ass_file(srt_path, ass_path, font='Arial', font_size=24, primary_color='&H00FFFFFF', outline_color='&H6600FFFF', back_color='&H6600FFFF', border_style=3, outline=1, shadow=0):
    ass_content = f"""[Script Info]
Title: Styled Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{font_size},{primary_color},{back_color},{outline_color},{back_color},-1,0,0,0,100,100,0,0,{border_style},{outline},{shadow},2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(srt_path, "r", encoding="utf-8") as f:
        subtitles = list(srt.parse(f.read()))

    for subtitle in subtitles:
        start = timedelta_to_ass_time(subtitle.start)
        end = timedelta_to_ass_time(subtitle.end)
        text = subtitle.content.replace('\n', '\\N')  # Replace new lines with ASS line breaks
        ass_content += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)


srt_path = "split_subtitles.srt"
ass_path = "styled_subtitles_test.ass"

if __name__ == "__main__":
    create_ass_file(srt_path, ass_path)
