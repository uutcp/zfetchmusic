import yt_dlp
import argparse
import os
import sys
import shutil
import subprocess
import re 

def time_to_cue_index(tstr):
    parts = list(map(int, tstr.strip().split(":")))
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h = 0
        m, s = parts
    else:
        raise ValueError("Invalid time format")
    total_min = h * 60 + m
    return f"{total_min:02}:{s:02}:00"


def generate_cue(intput_file, output_cue, audio_filename):
    with open(intput_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    output = []
    # output.append('PERFORMER "Various Artists"')
    output.append('TITLE "Hong Kong Movie Songs"')
    output.append(f'FILE "{audio_filename}" MP3\n')

    for idx, line in enumerate(lines):
        match = re.match(r".*?(\d{1,2}:\d{2}(?::\d{2})?)\s+(.*)", line)
        if not match:
            continue

        print(match.groups())

        time_str, title = match.groups()

        parts = re.split(r"-|\s+", title, maxsplit=1)
        print(title, parts)


        title = parts[0].strip()
        performer = parts[1].strip() if len(parts) > 1 else ""
        track_num = f"{idx+1:02}"
        index_time = time_to_cue_index(time_str)

        


        output.append(f'  TRACK {track_num} AUDIO')
        output.append(f'    TITLE "{title}"')
        output.append(f'    PERFORMER "{performer}"')
        output.append(f'    INDEX 01 {index_time}\n')

    with open(output_cue, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("CUE file generated as output.cue")

def print_comment_thread(comment):
    author = comment.get('author') or 'unknown'
    text = comment.get('text') or ''
    print(f"Pinned by {author}: {text}")
    for reply in comment.get('replies') or []:
        reply_author = reply.get('author') or 'unknown'
        reply_text = reply.get('text') or ''
        print(f"  Reply by {reply_author}: {reply_text}")

def download_audio_from_youtube(url, output_path, proxy=None):
    def progress_hook(d):
        if d.get('status') == 'downloading':
            downloaded = d.get('downloaded_bytes') or 0
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            if total:
                percent = downloaded / total * 100
                line = f"\rDownloading: {percent:5.1f}% ({downloaded}/{total} bytes)"
            else:
                line = f"\rDownloading: {downloaded} bytes"
            sys.stdout.write(line)
            sys.stdout.flush()
        elif d.get('status') == 'finished':
            sys.stdout.write("\nDownload finished, processing...\n")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        # 'quiet': True,
        'no_warnings': True,
        "proxy": proxy,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def ensure_local_mp3splt():
    local_path = os.path.join(os.path.dirname(__file__), "mp3splt")
    if os.path.isfile(local_path) and os.access(local_path, os.X_OK):
        return local_path

    brew_path = shutil.which("brew")
    if not brew_path:
        raise RuntimeError("Homebrew not found; install brew or place ./mp3splt locally.")

    if not shutil.which("mp3splt"):
        subprocess.run([brew_path, "install", "mp3splt"], check=True)

    system_mp3splt = shutil.which("mp3splt")
    if not system_mp3splt:
        raise RuntimeError("mp3splt not available after brew install.")

    shutil.copy2(system_mp3splt, local_path)
    os.chmod(local_path, 0o755)
    return local_path


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Download audio from YouTube videos.")
    argparser.add_argument("url", help="YouTube video URL")
    argparser.add_argument("-o", "--output", default="./outdir", help="Output directory")
    argparser.add_argument("-p", "--port", type=int, default=10700, help="Port number for the server (default: 10700)")
    # argparser.add_argument("--show-pinned", action="store_true", help="Print pinned comment (if available)")
    argparser.add_argument("--splitinfo", default="", help="Path to split info file")
    argparser.add_argument("--proxy", default="", help="Proxy server (e.g., 'http://proxyserver:port')")
    args = argparser.parse_args()

    # tempdir = tempfile.TemporaryDirectory()
    if args.output is None or args.output == "":
        args.output = "./outdir"
    os.makedirs(args.output, exist_ok=True)
    tempdir = args.output
    _mp3 = os.path.join(tempdir, "temp_audio.mp3")
    download_audio_from_youtube(args.url, os.path.splitext(_mp3)[0], args.proxy)

    if args.splitinfo and os.path.isfile(args.splitinfo):
        mp3splt_path = ensure_local_mp3splt()   
        cur = os.path.join(tempdir, "output.cue")
        generate_cue(args.splitinfo, cur, os.path.basename(_mp3))
        print("CUE file generated as output.cue")
        output_dir = args.output
        if not output_dir or not (output_dir.endswith(os.sep) or os.path.isdir(output_dir)):
            output_dir = os.path.dirname(output_dir) or "."
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run([mp3splt_path, "-c", cur, "-o", "@t", "-d", output_dir, _mp3], check=True)
        print(f"Split audio files saved to {output_dir}")
        os.remove(cur)
        os.remove(_mp3)