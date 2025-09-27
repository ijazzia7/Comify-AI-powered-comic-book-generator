from flask import Flask, render_template, jsonify, request
import requests, os
from comicBook import generate_comic_content, generate_image, generate_cover_propmt, return_pages, cover_generation
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import time
import uuid
import json


COMICS_DB = "comics.json"

f_path = "/Users/ijazulhaq/Downloads/strawberry-muffins/Strawberry Muffins Demo.ttf"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/comicgenerator")
def comicgenerator():
    return render_template("comicgenerator.html")

@app.route("/comicLibrary")
def comiclibrary():
    return render_template("comicLibrary.html")

@app.route("/comics", methods=["GET"])
def get_comics():
    if os.path.exists(COMICS_DB):
        with open(COMICS_DB, "r") as f:
            comics = json.load(f)
    else:
        comics = []
    return jsonify(comics)

@app.route("/comics/<comic_id>", methods=["GET"])
def get_comic(comic_id):
    if os.path.exists(COMICS_DB):
        with open(COMICS_DB, "r") as f:
            comics = json.load(f)
            comic = next((c for c in comics if c["id"] == comic_id), None)
            if comic:
                return jsonify(comic)
    return jsonify({"error": "Comic not found"}), 404


@app.route("/comicreader")
def comicreader():
    return render_template("comicreader.html")

@app.route("/generate_comic", methods=["POST"])
def api_generate_comic():
    data = request.get_json()
    idea = data.get("idea", "")

    if not idea:
        return jsonify({"error": "No idea provided"}), 400
    
    comic = generate(idea) 
    print(comic)
    # with open(COMICS_DB, "r") as f:
    #         comics = json.load(f)
    #         comic = comics[-1]   # get last comic in the list
    #         print(comic)
    return jsonify({"success": True, "id": comic["id"]})




def save_comic_metadata(comic_id, title, genre, pages):
    comic_entry = {
        "id": comic_id,
        "title": title,
        "createdAt": time.time(),
        "pages": pages,
        "genre": genre
    }

    if os.path.exists(COMICS_DB):
        with open(COMICS_DB, "r") as f:
            comics = json.load(f)
    else:
        comics = []

    comics.append(comic_entry)

    with open(COMICS_DB, "w") as f:
        json.dump(comics, f, indent=2)

    return comic_entry



def generate(idea):
    title, texts, vis, text_context = generate_comic_content(idea)
    cover_prompt_for_schnell, genre = generate_cover_propmt(text_context)
    
    comic_id = str(uuid.uuid4())
    base_dir = os.path.join("static", "comics", comic_id)
    output_dir = os.path.join(base_dir, "output_images")
    pages_dir = os.path.join(base_dir, "pages")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(pages_dir, exist_ok=True)
    
    # Generate interior images
    for i in tqdm(range(len(vis))):
        if i in range(2, 4):
            img = generate_image(vis[i], width=620, height=300)
        else:
            img = generate_image(vis[i])
        img.save(os.path.join(output_dir, f"image_{i}.jpg"))
            
    # Generate cover
    cover_img_raw = generate_image(cover_prompt_for_schnell, width=700, height=1040)
    cover_path = os.path.join(output_dir, "cover_image.jpg")
    cover_img_raw.save(cover_path)
    
    # Generate text pages
    cover_page = cover_generation(title, genre, cover_path)
    page1, page2, page3 = return_pages(texts, output_dir)
    cover_page_path = os.path.join(pages_dir, "01.jpg")
    page1_path = os.path.join(pages_dir, "02.jpg")
    page2_path = os.path.join(pages_dir, "03.jpg")
    page3_path = os.path.join(pages_dir, "04.jpg")
    cover_page.save(cover_page_path)
    page1.convert("RGB").save(page1_path)
    page2.convert("RGB").save(page2_path)
    page3.convert("RGB").save(page3_path)
    
    # Save metadata for library
    return save_comic_metadata(
        comic_id,
        title,
        genre,
        pages=[
            {"imageUrl": f"/{cover_page_path}"},
            {"imageUrl": f"/{page1_path}"},
            {"imageUrl": f"/{page2_path}"},
            {"imageUrl": f"/{page3_path}"},
            {"imageUrl": f"/static/pages/05.jpg"},
            {"imageUrl": f"/static/pages/06.jpg"}
        ]
    )






if __name__ == '__main__':
    app.run(debug=True)
