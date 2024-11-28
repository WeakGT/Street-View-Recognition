from pydub import AudioSegment

# 載入音效文件
input_path = "" # Path to the audio file
output_path = "" # Path to the output audio file

# 使用 pydub 重新匯出為 PCM WAV 格式
sound = AudioSegment.from_file(input_path)
sound.export(output_path, format="wav", codec="pcm_s16le")  # PCM 16-bit 格式

print(f"File has been successfully exported to {output_path}")