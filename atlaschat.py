import torch
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="MBZUAI-Paris/Atlas-Chat-27B",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda" # replace with "mps" to run on a Mac device
)

messages = [
    {"role": "user", "content": 'شكون لي صنعك؟'},
]

outputs = pipe(messages, max_new_tokens=256, temperature=0.0)
assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
print(assistant_response)
