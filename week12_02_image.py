from openai import OpenAI
import base64

client = OpenAI()

prompt="A futuristic view of Atlanta at night with purple sky"
result = client.images.generate(
    model="gpt-image-1.5",
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("atlanta.png", "wb") as f:
    f.write(image_bytes)

# gpt-image-1
# gpt-image-1.5
# gpt-image-1-mini