import pickle
from transformers import pipeline
from sklearn.metrics import classification_report
import numpy as np


concepts=['sexual', 'nude','gore','violence']

classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli", )

def is_nsfw(prompt):

      output = classifier(prompt, concepts, multi_label=True,device='cuda')
      return (np.array(output["scores"])>0.95).any()


