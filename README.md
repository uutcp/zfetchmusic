# zmusic-fetch

A tool to extract audio from videos and automatically split it into multiple audio files based on timestamp information.

## Features

- 🎵 Download audio from videos (using yt-dlp)
- ✂️ Automatically split audio based on timestamp information
- 🌐 Proxy support

## Requirements

- Python 3.x
- yt-dlp
- mp3splt 
- FFmpeg

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

## Disclaimer

This tool is for educational and personal use only. Use it only if you have the rights to the content and comply with platform terms and local laws. The developers are not responsible for misuse.
