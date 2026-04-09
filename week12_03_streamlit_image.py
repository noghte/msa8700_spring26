import os
import base64
from datetime import datetime

import requests
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OLLAMA_URL = "http://10.230.100.240:17020/api/generate"

def refine_image_prompt_with_openai(user_prompt: str, style: str) -> str:
    style_text = "" if style == "None" else f"Preferred visual style: {style}."

    response = client.responses.create(
        model="gpt-4o",
        instructions=(
            "You are an expert prompt writer for image generation. "
            "Rewrite the user's request into one strong, vivid, detailed prompt for image generation. "
            "Keep the original meaning. Improve clarity, composition, subject detail, lighting, mood, "
            "camera/viewpoint if relevant, and artistic direction. "
            "Return only the final prompt text. Do not explain anything."
        ),
        input=f"User request: {user_prompt}\n{style_text}"
    )

    return response.output_text.strip()

def refine_image_prompt(user_prompt: str, style: str) -> str:
    style_text = "" if style == "None" else f"Preferred visual style: {style}."

    ollama_prompt = f"""
You are an expert prompt writer for image generation models.

Rewrite the user's request into one strong, vivid, detailed image-generation prompt.
Keep the meaning the same, but improve clarity, visual detail, composition, lighting, mood, and artistic direction.
Return only the final prompt text.
Do not include explanations.
Do not include bullet points.

User request: {user_prompt}
{style_text}
""".strip()

    data = {
        "model": "gpt-oss:20b",
        "prompt": ollama_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=data)
    response.raise_for_status()

    refined_prompt = response.json()["response"].strip()
    return refined_prompt

# Page setup
st.set_page_config(page_title="OpenAI Image Generator", page_icon="🖼️", layout="centered")
st.title("OpenAI Image Generator")

# Create client
client = OpenAI()

# UI
prompt = st.text_area(
    "Enter your prompt",
    placeholder="A futuristic view of Atlanta at night with purple sky",
    height=120,
)

model = st.selectbox(
    "Select model",
    [
        "gpt-image-1",
        "gpt-image-1.5",
        "gpt-image-1-mini",
    ],
)

style = st.selectbox(
    "Select art style",
    [
        "None",
        "Photorealistic",
        "Painting",
        "Sketch",
        "Cartoon",
    ],
)

generate_button = st.button("Generate Image", type="primary")

# Output directory
OUTPUT_DIR = "generated_images"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_image_with_timestamp(image_bytes: bytes, model_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model_name = model_name.replace(".", "_")
    filename = f"generated_{safe_model_name}_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    return filepath


if generate_button:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            
            # final_prompt = refine_image_prompt(prompt, style)
            final_prompt = refine_image_prompt_with_openai(prompt, style)
            st.subheader("Refined prompt")
            st.write(final_prompt)

            with st.spinner("Generating image..."):
                result = client.images.generate(
                    model=model,
                    prompt=final_prompt,
                )

                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)
                image_base64_str = base64.b64encode(image_bytes).decode("utf-8")
                image_data_url = f"data:image/png;base64,{image_base64_str}"

                saved_path = save_image_with_timestamp(image_bytes, model)

            st.success("Image generated successfully.")
            st.write(f"Saved to: `{saved_path}`")
            st.image(image_bytes, caption=f"Generated with {model} ({style})" , use_container_width=True)

            facebook_share_url = f"https://www.facebook.com/sharer/sharer.php?u={image_data_url}"

            st.markdown(
                f"""
                <a href="{facebook_share_url}" target="_blank">
                    <button style="
                        background-color:#1877F2;
                        color:white;
                        border:none;
                        padding:10px 16px;
                        border-radius:6px;
                        font-size:16px;
                        cursor:pointer;
                    ">
                        Share on Facebook
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error: {e}")