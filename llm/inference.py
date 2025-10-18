from transformers import pipeline

# Load once at startup
summarizer = pipeline(
    "text2text-generation",
    model="Falconsai/medical_summarization",
    device_map="auto"
)
