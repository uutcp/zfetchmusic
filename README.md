# zmusic-fetch

A tool to extract audio from YouTube/Bilibili videos and automatically split it into multiple audio files based on timestamp information.

## Features

- 🎵 Download audio from YouTube/Bilibili videos (MP3 format)
- ✂️ Automatically split audio based on timestamp information
- 📝 Auto-generate CUE files
- 🌐 Proxy support
- 🎯 Automatic mp3splt management

## Requirements

- Python 3.x
- yt-dlp
- mp3splt (automatically installed via Homebrew on macOS)
- FFmpeg (for audio format conversion)

## Installation

1. Clone or download this project

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (if not already installed):
```bash
brew install ffmpeg
```

4. mp3splt will be automatically installed via Homebrew on first run

## Usage

### Basic Usage

Download audio without splitting:
```bash
python zgetmusic.py <video_URL>
```

### Download and Split Audio

```bash
python zgetmusic.py <video_URL> --splitinfo <timestamp_file>
```

### Complete Example

```bash
python zgetmusic.py https://www.bilibili.com/video/BV18oqQBdEnr?t=14.2 --splitinfo 1.txt
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `url` | - | Video URL (required) | - |
| `--output` | `-o` | Output directory | `./outdir` |
| `--splitinfo` | - | Timestamp file path | - |
| `--proxy` | - | Proxy server address | - |
| `--port` | `-p` | Port number | `10700` |

## Timestamp File Format

Create a text file (e.g., `1.txt`) with one timestamp and song info per line:

```
0:00 Song Title - Artist Name
2:30 Another Song - Another Artist
5:15:20 Third Song - Artist Name
```

Supported time formats:
- `M:SS` (minutes:seconds)
- `H:MM:SS` (hours:minutes:seconds)

## Output

- Without splitting: Generates `temp_audio.mp3` in the output directory
- With splitting: Generates multiple MP3 files named after each track in the output directory

## Using a Proxy

To use a proxy (e.g., for accessing restricted content):

```bash
python zgetmusic.py <video_URL> --proxy http://127.0.0.1:7890 --splitinfo 1.txt
```

## Notes

- Ensure sufficient disk space for downloaded audio files
- Timestamp file must be UTF-8 encoded
- After splitting is complete, the original audio file and CUE file are automatically deleted

## License

This project is for educational and personal use only. Please comply with the terms of service of the respective video platforms.
