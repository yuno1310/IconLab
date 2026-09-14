"""Assemble 180-second narrated evidence replays from captured app/deck frames."""
import json
import subprocess
import sys
import wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/media-deps'))
import imageio_ffmpeg
encoder=imageio_ffmpeg.get_ffmpeg_exe()
chapters=json.loads((ROOT/'tmp/narration.json').read_text(encoding='utf-8'))
(ROOT/'output/videos').mkdir(exist_ok=True)
def stamp(seconds):
    ms=round(seconds*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
for name,texts in chapters.items():
    waves=[]; durations=[]
    for i in range(7):
        with wave.open(str(ROOT/f'tmp/audio/{name}-{i}.wav')) as w:
            params=w.getparams(); data=w.readframes(w.getnframes()); waves.append(data); durations.append(w.getnframes()/w.getframerate())
    remaining=180-sum(durations)
    if remaining<0: raise ValueError('Narration exceeds 180 seconds')
    silence=remaining/7
    total_audio=ROOT/f'tmp/audio/{name}-full.wav'
    with wave.open(str(total_audio),'wb') as w:
        w.setparams(params)
        for data in waves:
            w.writeframes(data);w.writeframes(b'\0'*round(silence*params.framerate)*params.sampwidth*params.nchannels)
    frames=[ROOT/f'tmp/decks/{name}-1.png',ROOT/('tmp/decks/assignment-04-2.png' if name=='assignment-04' else 'tmp/viewer-easy.png'),ROOT/'tmp/viewer-conflict.png',ROOT/'tmp/viewer-refusal.png',ROOT/'tmp/viewer-scores.png',ROOT/'tmp/viewer-security.png',ROOT/f'tmp/decks/{name}-6.png']
    concat=[]; subtitles=[]; position=0
    for i,(frame,duration,text) in enumerate(zip(frames,durations,texts)):
        seconds=duration+silence
        concat.extend([f"file '{frame.as_posix()}'",f'duration {seconds:.6f}'])
        # Subtitle chapters provide a complete transcript without burning tiny text onto evidence.
        subtitles.extend([str(i+1),f'{stamp(position)} --> {stamp(position+duration)}',text,''])
        position+=seconds
    concat.append(f"file '{frames[-1].as_posix()}'")
    manifest=ROOT/f'tmp/{name}-frames.txt';manifest.write_text('\n'.join(concat))
    (ROOT/f'output/videos/{name}.srt').write_text('\n'.join(subtitles),encoding='utf-8')
    output=ROOT/f'output/videos/{name}.mp4'
    subprocess.run([encoder,'-y','-loglevel','error','-f','concat','-safe','0','-i',str(manifest),'-i',str(total_audio),'-t','180','-r','10','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',str(output)],check=True)
    print(name,output.stat().st_size,flush=True)
