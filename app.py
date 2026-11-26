import os
import uuid
import asyncio
from pathlib import Path
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont, ImageOps
import edge_tts
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "static" / "uploads"
OUTPUT_DIR = ROOT / "static" / "outputs"
WORK_DIR = ROOT / "work"
for folder in (UPLOAD_DIR, OUTPUT_DIR, WORK_DIR):
    folder.mkdir(parents=True, exist_ok=True)

ALLOWED = {".png", ".jpg", ".jpeg", ".webp"}
W, H = 1080, 1920

def get_font(size):
    # Put NotoSansTelugu-Regular.ttf in the project root for Telugu text.
    candidates = [
        ROOT / "NotoSansTelugu-Regular.ttf",
        Path("/usr/share/fonts/truetype/noto/NotoSansTelugu-Regular.ttf"),
        Path("/usr/share/fonts/truetype/noto/NotoSansTeluguUI-Regular.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]

def make_scene_card(text, image_path, out_path, title, index):
    if image_path and Path(image_path).exists():
        bg = Image.open(image_path).convert("RGB")
        bg = ImageOps.fit(bg, (W, H), method=Image.Resampling.LANCZOS)
        # Dark overlay improves readability.
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 125))
        bg = Image.alpha_composite(bg.convert("RGBA"), overlay)
    else:
        bg = Image.new("RGBA", (W, H), (10, 35, 75, 255))

    draw = ImageDraw.Draw(bg)
    title_font = get_font(62)
    body_font = get_font(48)
    small_font = get_font(30)

    draw.rounded_rectangle((55, 90, W-55, 300), radius=35, fill=(5, 20, 50, 205))
    draw.text((95, 145), title[:32], font=title_font, fill="white")

    lines = wrap_text(draw, text, body_font, W-180)
    line_height = 78
    total_height = len(lines) * line_height
    y = max(430, (H-total_height)//2)
    draw.rounded_rectangle((65, y-55, W-65, min(H-250, y+total_height+65)),
                           radius=32, fill=(0, 0, 0, 155))
    for line in lines:
        draw.text((105, y), line, font=body_font, fill="white", stroke_width=1, stroke_fill="black")
        y += line_height

    draw.text((75, H-150), f"SVSC Video Creator  |  Scene {index}", font=small_font, fill=(235,235,235))
    bg.convert("RGB").save(out_path, quality=92)

async def make_tts(text, path, voice):
    communicator = edge_tts.Communicate(text=text, voice=voice, rate="+0%")
    await communicator.save(str(path))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title", "SVSC Video").strip() or "SVSC Video"
        voice = request.form.get("voice", "te-IN-ShrutiNeural")
        ratio = request.form.get("ratio", "9:16")
        raw_scenes = request.form.get("scenes", "")
        scenes = [s.strip() for s in raw_scenes.splitlines() if s.strip()]
        if not scenes:
            flash("దయచేసి కనీసం ఒక సీన్ స్క్రిప్ట్ ఇవ్వండి.")
            return redirect(url_for("home"))

        uploaded = request.files.getlist("images")
        image_paths = []
        for file in uploaded:
            if file and file.filename:
                ext = Path(secure_filename(file.filename)).suffix.lower()
                if ext in ALLOWED:
                    name = f"{uuid.uuid4().hex}{ext}"
                    dest = UPLOAD_DIR / name
                    file.save(dest)
                    image_paths.append(str(dest))

        job = uuid.uuid4().hex
        clips, audio_files, image_files = [], [], []
        try:
            for i, scene_text in enumerate(scenes, start=1):
                audio_path = WORK_DIR / f"{job}_{i}.mp3"
                image_path = WORK_DIR / f"{job}_{i}.jpg"
                asyncio.run(make_tts(scene_text, audio_path, voice))
                make_scene_card(scene_text, image_paths[i-1] if i <= len(image_paths) else None,
                                image_path, title, i)
                audio = AudioFileClip(str(audio_path))
                clip = ImageClip(str(image_path)).with_duration(audio.duration).with_audio(audio)
                clips.append(clip)
                audio_files.append(audio_path)
                image_files.append(image_path)

            final = concatenate_videoclips(clips, method="compose")
            if ratio == "16:9":
                final = final.resized(height=1080).cropped(x_center=final.w/2, y_center=final.h/2, width=1920, height=1080)
            output_name = f"SVSC_{job}.mp4"
            output_path = OUTPUT_DIR / output_name
            final.write_videofile(str(output_path), fps=24, codec="libx264", audio_codec="aac",
                                  preset="medium", logger=None)
            final.close()
            for clip in clips:
                clip.close()
            return render_template("result.html", video=url_for("static", filename=f"outputs/{output_name}"),
                                   filename=output_name)
        except Exception as exc:
            for clip in clips:
                try: clip.close()
                except: pass
            flash(f"వీడియో తయారీలో సమస్య: {exc}. FFmpeg మరియు Telugu font సరిగా ఇన్‌స్టాల్ అయ్యాయో చూడండి.")
            return redirect(url_for("home"))
        finally:
            for p in audio_files + image_files:
                try: Path(p).unlink(missing_ok=True)
                except: pass

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
