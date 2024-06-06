import streamlit as st
import torch
import numpy as np
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from accelerate import Accelerator
from preprocess import preprocess_text
from zeroshot import is_nsfw

# Initialize the accelerator
accelerator = Accelerator()

# Set device (GPU if available, otherwise CPU)
device = accelerator.device

# Clear CUDA cache to free up memory
torch.cuda.empty_cache()

# Create a mapping between the model names and the display names
model_options = {
    "eliasalbouzidi/distilbert-nsfw-text-classifier": "DistilBert - 67M",
    "eliasalbouzidi/roberta-512-fbeta1.6-learning1": "RoBerta - 125M",
    "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli": "DeBERTa (Zero Shot) - 180M "
}
concepts=['sexual', 'nude','gore','violence']

# Streamlit app title & image
st.image("banner.PNG")

# Text input for the prompt
prompt = st.text_input("Enter a prompt:")

# Number of images to generate
num_images = st.number_input("Enter the number of images to generate:", min_value=1, max_value=10)

# Add a selectbox to choose the filter
filter_option = st.selectbox("Choose the filter:", list(model_options.values()))

# Get the corresponding model name
model_name = list(model_options.keys())[list(model_options.values()).index(filter_option)]

# Add a checkbox to enable or disable the NSFW filter for each image
nsfw_filter_enabled = st.checkbox("Enable NSFW filter for each image")

# Add a checkbox to enable or disable the preprocessing stage
preprocessing_enabled = st.checkbox("Enable preprocessing stage")

# Initialize the text classification pipeline with device and the selected model
if model_name != "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli":
    pipe = pipeline("text-classification", model=model_name, device=0 if torch.cuda.is_available() else -1)
else:
    classifier = pipeline("zero-shot-classification", model=model_name, device=0 if torch.cuda.is_available() else -1)

# Generate image button
generate_button = st.button("Generate Images")

if generate_button and prompt and num_images > 0:

    # Initialize the diffusion pipeline and move it to the specified device for each image
    for i in range(num_images):
        diffusion_pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", safety_checker=None)
        diffusion_pipeline.to(device)
        diffusion_pipeline = accelerator.prepare(diffusion_pipeline)

        if preprocessing_enabled:
            # Preprocess the prompt if the preprocessing stage is enabled
            prompt = preprocess_text(prompt)

        if nsfw_filter_enabled:
            # Run the text classification pipeline
            if model_name != "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli":
                res = pipe(prompt)[0]['label']
            else:
                output = classifier(prompt, concepts, multi_label=True, device='cuda')
                res = 'nsfw' if (np.array(output["scores"])>0.95).any() else 'safe'

            if res == 'safe':
                # Generate the image if the content is safe
                with torch.no_grad():
                    try:
                        torch.cuda.empty_cache()
                        image = diffusion_pipeline(prompt, num_inference_steps=25, height=512, width=512).images[0]  # Reduce inference steps and image size
                        st.image(image, caption=f"Generated Image {i+1}")
                        torch.cuda.empty_cache()
                    except torch.cuda.OutOfMemoryError:
                        st.error("CUDA out of memory. Try reducing the input size or inference steps.")
                        torch.cuda.empty_cache()
            else:
                # Show an attention image if the content is NSFW
                st.image("AttentionImage.PNG", caption=f"NSFW Content Detected {i+1}")
        else:
            # Generate the image without the NSFW filter
            with torch.no_grad():
                try:
                    torch.cuda.empty_cache()
                    image = diffusion_pipeline(prompt, num_inference_steps=25, height=512, width=512).images[0]  # Reduce inference steps and image size
                    st.image(image, caption=f"Generated Image {i+1}")
                    torch.cuda.empty_cache()
                except torch.cuda.OutOfMemoryError:
                    st.error("CUDA out of memory. Try reducing the input size or inference steps.")
                    torch.cuda.empty_cache()
