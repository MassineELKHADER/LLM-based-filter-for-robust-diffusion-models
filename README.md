# Streamlit App for LLM based filter for detecting sensitive content when generating images

## Description
This Streamlit app allows users to generate images based on prompts using various models. The prompt passes through a filter (if enabled), and if it does not contain sensitive content, it proceeds to the diffusion model later in the pipeline. The diffusion model is based on **Stable Diffusion** from Hugging Face's platform, which can be found [here](https://huggingface.co/CompVis/stable-diffusion-v1-4).

## Functionalities
- Generate up to 10 images for a given prompt.
- Select from three different models, including fine-tuned and zero-shot models.
- Toggle button to enable or disable the filter, demonstrating the model's capability to identify sensitive content.
- Toggle button to enable or disable the pre-processing stage.

## Usage
To run the app locally, use the following command:
python3 -m streamlit run app.py


