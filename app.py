from flask import Flask, render_template, jsonify, request
import requests, os
from comicBook import generate_comic_content, generate_image, generate_cover_propmt, return_pages, cover_generation
from PIL import Image, ImageDraw, ImageFont
f_path = "/Users/ijazulhaq/Downloads/strawberry-muffins/Strawberry Muffins Demo.ttf"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/comicgenerator")
def comicgenerator():
    return render_template("comicgenerator.html")

@app.route("/comicreader")
def comicreader():
    return render_template("comicreader.html")

@app.route("/api/generate_comic", methods=["POST"])
def api_generate_comic():
    data = request.get_json()
    idea = data.get("idea", "")

    if not idea:
        return jsonify({"error": "No idea provided"}), 400

    try:
        # === your generation pipeline ===
        title, texts, vis, text_context = generate_comic_content(idea)
        cover_prompt_for_schnell, genre = generate_cover_propmt(text_context)

        output_images = []
        for i in range(len(vis)):
            if i in range(2, 4):
                img = generate_image(vis[i], width=620, height=300)
            else:
                img = generate_image(vis[i])
            img_path = f'static/output_images/image_{i}.jpg'
            img.save(img_path)
            output_images.append(img_path)

        cover_path = 'static/output_images/cover_image.jpg'
        img = generate_image(cover_prompt_for_schnell, width=700, height=1040)
        img.save(cover_path)

        cover_generation(title, genre)
        page1, page2, page3 = return_pages(texts)
        page_paths = [
            'static/pages/02.jpg',
            'static/pages/03.jpg',
            'static/pages/04.jpg'
        ]
        page1.convert('RGB').save(page_paths[0])
        page2.convert('RGB').save(page_paths[1])
        page3.convert('RGB').save(page_paths[2])

        return jsonify({
            "title": title,
            "genre": genre,
            "cover": cover_path,
            "images": output_images,
            "pages": page_paths,
            "texts": texts
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def generate(idea):
    title, texts, vis, text_context = generate_comic_content(idea)
    cover_prompt_for_schnell, genre = generate_cover_propmt(text_context)
    for i in range(len(vis)):
        if i in range(2,4):
            img = generate_image(vis[i], width=620, height=300)
            img.save(f'static/output_images/image_{i}.jpg')
        else:
            img = generate_image(vis[i])
            img.save(f'static/output_images/image_{i}.jpg')
            
    img = generate_image(cover_prompt_for_schnell, width=700, height=1040)
    img.save(f'static/output_images/cover_image.jpg')
    
    cover_generation(title, genre)
    page1, page2, page3 = return_pages(texts)
    page1.convert('RGB').save('static/pages/02.jpg')
    page2.convert('RGB').save('static/pages/03.jpg')
    page3.convert('RGB').save('static/pages/04.jpg')
    







if __name__ == '__main__':
    app.run(debug=True)
