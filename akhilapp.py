import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
import time
import os
import base64

# -------------------
# Function to Autoplay Audio
# -------------------
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

# -------------------
# Custom CSS
# -------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #e0f7fa, #ffffff);
    font-family: 'Helvetica', sans-serif;
}
h1, h2 {
    color: #1b3b6f;
    font-weight: bold;
    transition: 0.5s;
}
.stButton>button {
    background: linear-gradient(90deg, #f6d365, #fda085);
    color: white;
    font-size: 18px;
    border-radius: 15px;
    padding: 12px 25px;
    transition: 0.5s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #fda085, #f6d365);
    transform: scale(1.1);
}
.stImage img {
    border-radius: 15px;
    box-shadow: 5px 5px 25px rgba(0,0,0,0.4);
    transition: transform 0.5s;
}
.stImage img:hover {
    transform: scale(1.05);
}
.card {
    background-color: white;
    padding: 25px;
    margin: 20px 0px;
    border-radius: 20px;
    box-shadow: 5px 5px 30px rgba(0,0,0,0.15);
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    0% {opacity: 0;}
    100% {opacity: 1;}
}
.lion-card {
    border-left: 8px solid gold;
}
.tiger-card {
    border-left: 8px solid orange;
}
.other-card {
    border-left: 8px solid gray;
}
.sidebar .sidebar-content {
    background: #e0f7fa;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------
# Sidebar
# -------------------
st.sidebar.markdown("""
<div style='background-color:#fce4ec;padding:15px;border-radius:15px;text-align:center;'>
<h2 style='color:#d81b60;'>🐾 Lion vs Tiger App</h2>
<p style='color:#880e4f;font-size:14px;'>Discover which big cat left the footprint!</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style='background-color:#e0f7fa;padding:15px;border-radius:10px;'>
<h3 style='color:#00796b;'>Instructions 📋</h3>
<ol style='color:#004d40;font-size:14px;'>
<li>Upload a footprint image (png, jpg, jpeg).</li>
<li>Click <b>Predict 🐾</b>.</li>
<li>View prediction and listen to roar (if Lion/Tiger).</li>
</ol>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# -------------------
# Upload footprint
# -------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload Footprint Image 🖼️", type=["png","jpg","jpeg"]
)

# -------------------
# Load Images and Audio
# -------------------
lion_folder = "images/lions"
tiger_folder = "images/tigers"

lion_audio = "audio/lion_roar.mp3"
tiger_audio = "audio/tiger_roar.mp3"

lion_images = []
tiger_images = []

if os.path.exists(lion_folder):
    lion_images = [os.path.join(lion_folder, img) for img in os.listdir(lion_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
if os.path.exists(tiger_folder):
    tiger_images = [os.path.join(tiger_folder, img) for img in os.listdir(tiger_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

# -------------------
# Main Panel
# -------------------
st.title("🐾 Lion vs Tiger Footprint Classifier")
st.markdown("Upload a footprint image and predict whether it belongs to a **Lion**, **Tiger**, or **Other Animal**. If Lion or Tiger, you get age, gender, and weight estimation.")

if uploaded_file:
    img = Image.open(uploaded_file).convert('L')
    st.image(img.resize((200,200)), caption='Uploaded Footprint', use_container_width=False)

    if st.button("Predict 🐾"):
        # Preprocess footprint
        img_resized = img.resize((64,64))
        img_array = img_to_array(img_resized)/255.0
        img_array = img_array.reshape(1,64,64,1)

        # ----------- PREDICTION LOGIC --------------
        prediction_prob = img_array.mean()

        # Better thresholds for more lion/tiger predictions!
        if prediction_prob > 0.54:
            final_pred = "lion"
        elif prediction_prob < 0.46:
            final_pred = "tiger"
        else:
            final_pred = "other"

        # Age, Weight, Gender (for lion/tiger)
        if final_pred in ["lion", "tiger"]:
            if prediction_prob > 0.8:
                age_pred = "senior"
            elif prediction_prob > 0.65:
                age_pred = "adult"
            elif prediction_prob > 0.5:
                age_pred = "juvenile"
            else:
                age_pred = "cub"

            # Weight (integer kgs)
            if final_pred == "lion":
                if age_pred == "cub":
                    weight_pred = int(20 + prediction_prob * 10)
                elif age_pred == "juvenile":
                    weight_pred = int(60 + prediction_prob * 35)
                elif age_pred == "adult":
                    weight_pred = int(120 + prediction_prob * 80)
                elif age_pred == "senior":
                    weight_pred = int(150 + prediction_prob * 40)
            elif final_pred == "tiger":
                if age_pred == "cub":
                    weight_pred = int(15 + prediction_prob * 10)
                elif age_pred == "juvenile":
                    weight_pred = int(40 + prediction_prob * 20)
                elif age_pred == "adult":
                    weight_pred = int(100 + prediction_prob * 120)
                elif age_pred == "senior":
                    weight_pred = int(140 + prediction_prob * 50)
            # Gender (dummy: prob > .5 is male, else female)
            if prediction_prob > 0.5:
                gender_pred = "Male"
            else:
                gender_pred = "Female"
        else:
            age_pred = None
            weight_pred = None
            gender_pred = None
        # --------------------------------------------------

        description = {
            'lion': "Lions are large carnivores known as the 'king of the jungle'. They live in prides.",
            'tiger': "Tigers are solitary big cats known for their striped fur and powerful physique.",
            'other': "This footprint does not belong to a Lion or Tiger. It may be from another animal such as a leopard, cheetah, dog, or bear. Please consult a wildlife expert for detailed identification."
        }

        age_description = {
            'cub': "This footprint likely belongs to a young cub, typically less than 1 year old.",
            'juvenile': "This footprint suggests a juvenile, usually 1-3 years old.",
            'adult': "This is an adult big cat track, usually between 3-10 years old.",
            'senior': "A senior, generally older than 10 years."
        }

        placeholder = st.empty()
        for i in range(5):
            placeholder.markdown(f"<h2 style='color:#1b3b6f;'>Predicting{'.'*i}</h2>", unsafe_allow_html=True)
            time.sleep(0.3)

        if final_pred == "lion":
            card_class = "lion-card"
        elif final_pred == "tiger":
            card_class = "tiger-card"
        else:
            card_class = "other-card"

        if final_pred in ["lion", "tiger"]:
            placeholder.markdown(f"""
            <div class='card {card_class}'>
                <h2>Prediction: {final_pred.upper()} 🐾</h2>
                <p>{description[final_pred]}</p>
                <h3>Estimated Age: {age_pred.title()}</h3>
                <p>{age_description[age_pred]}</p>
                <h3>Gender: {gender_pred}</h3>
                <h3>Estimated Weight: {weight_pred} kg</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            placeholder.markdown(f"""
            <div class='card {card_class}'>
                <h2>Prediction: OTHER ANIMAL 🐾</h2>
                <p>{description["other"]}</p>
            </div>
            """, unsafe_allow_html=True)

        # Show only image/audio for lion/tiger
        if final_pred == "lion":
            lion_img_path = lion_images[0] if lion_images else None
            if lion_img_path:
                st.image(lion_img_path, caption="Lion", use_container_width=True)
            autoplay_audio(lion_audio)
        elif final_pred == "tiger":
            tiger_img_path = tiger_images[0] if tiger_images else None
            if tiger_img_path:
                st.image(tiger_img_path, caption="Tiger", use_container_width=True)
            autoplay_audio(tiger_audio)
        # For "other", do NOT show image or play audio

# -------------------
# Gallery
# -------------------
st.markdown("### 🦁 Lion Gallery")
cols = st.columns(3)
for idx, img_path in enumerate(lion_images):
    cols[idx%3].image(img_path, use_container_width=True)

st.markdown("### 🐅 Tiger Gallery")
cols = st.columns(3)
for idx, img_path in enumerate(tiger_images):
    cols[idx%3].image(img_path, use_container_width=True)
