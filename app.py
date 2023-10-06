from flask import Flask, request, render_template, send_file
from PIL import Image
import os

app = Flask(__name__)

# Set the desired size for the images
IMAGE_SIZE = (1024, 1024)
OVERLAYS_FOLDER = 'static/overlays/'
UPLOAD_FOLDER = 'static/uploads/'
COMPOSITION_FOLDER = 'static/compositions/'

# Ensure the composition folder exists
os.makedirs(COMPOSITION_FOLDER, exist_ok=True)

def resize_image(image, size):
    return image.resize(size, Image.ANTIALIAS)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'user_image' not in request.files:
            return "No file part"

        user_image = request.files['user_image']

        if user_image.filename == '':
            return "No selected file"

        # Save and process the uploaded image
        user_img = Image.open(user_image)
        user_img = resize_image(user_img, IMAGE_SIZE)

        # Open the overlay image (provided by you)
        overlay_img = Image.open(os.path.join(OVERLAYS_FOLDER, 'overlay.png'))
        overlay_img = resize_image(overlay_img, IMAGE_SIZE)

        # Apply the overlay
        composition = Image.alpha_composite(user_img.convert('RGBA'), overlay_img.convert('RGBA'))

        # Save the composition
        composition_path = os.path.join(COMPOSITION_FOLDER, 'result.png')
        composition.save(composition_path)

        return render_template('index.html', result=True)

    return render_template('index.html', result=False)

@app.route('/download')
def download():
    composition_path = os.path.join(COMPOSITION_FOLDER, 'result.png')
    return send_file(composition_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
