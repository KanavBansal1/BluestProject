from flask import Flask, render_template, request
import numpy as np
import random
import io
import base64
from PIL import Image

app = Flask(__name__)

# Note: synthetic data helps privacy

TEXT_TEMPLATES = [
    "The {adj} {noun} {verb} over the {noun2}.",
    "A {noun} can {verb} very {adv}.",
    "Many {noun}s {verb} in the {noun2}.",
    "It is {adj} that the {noun} {verb}s."
]
ADJECTIVES = ["quick", "lazy", "happy", "sad", "fast", "slow", "bright", "dark"]
NOUNS = ["fox", "dog", "cat", "bird", "tree", "car", "computer", "person"]
VERBS = ["jumps", "runs", "sleeps", "flies", "codes", "walks"]
ADVERBS = ["quickly", "slowly", "happily", "sadly", "well", "poorly"]

def generate_tabular(num_samples, target_mean, target_std):
    """Generate tabular numerical data using normal distribution."""
    synthetic_data = []
    for _ in range(num_samples):
        val1 = np.round(np.random.normal(target_mean, target_std), 2)
        val2 = np.round(np.random.normal(target_mean * 1.5, target_std * 0.8), 2)
        category = random.choice(["Type A", "Type B", "Type C"])
        synthetic_data.append({"val1": val1, "val2": val2, "category": category})
    return synthetic_data

def generate_text(num_samples, num_sentences):
    """Generate synthetic sentences randomly."""
    outputs = []
    for _ in range(num_samples):
        sentences = []
        for _ in range(num_sentences):
            template = random.choice(TEXT_TEMPLATES)
            sentence = template.format(
                adj=random.choice(ADJECTIVES),
                noun=random.choice(NOUNS),
                verb=random.choice(VERBS),
                noun2=random.choice(NOUNS),
                adv=random.choice(ADVERBS)
            )
            sentences.append(sentence.capitalize())
        outputs.append(" ".join(sentences))
    return outputs

def generate_image(num_samples, size):
    """Generate synthetic image using random noise."""
    outputs = []
    for _ in range(num_samples):
        # Generate random colored noise
        noise = np.random.randint(0, 256, (size, size, 3), dtype=np.uint8)
        img = Image.fromarray(noise)
        
        # Save to buffer and base64 encode
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode("utf-8")
        outputs.append(img_str)
    return outputs

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    data_type = "tabular" # default
    
    if request.method == "POST":
        data_type = request.form.get("data_type", "tabular")
        try:
            num_samples = int(request.form.get("num_samples", 10))
            
            if data_type == "tabular":
                target_mean = float(request.form.get("target_mean", 50.0))
                target_std = float(request.form.get("target_std", 15.0))
                output = {"type": "tabular", "data": generate_tabular(num_samples, target_mean, target_std)}
                
            elif data_type == "text":
                num_sentences = int(request.form.get("num_sentences", 5))
                output = {"type": "text", "data": generate_text(num_samples, num_sentences)}
                
            elif data_type == "image":
                img_size = int(request.form.get("img_size", 256))
                output = {"type": "image", "data": generate_image(num_samples, img_size)}
                
        except ValueError:
            pass
            
    return render_template("index.html", output=output, data_type=data_type)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
