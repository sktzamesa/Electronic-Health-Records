# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from transformers import pipeline
from .models import MedicalReport

summarizer = pipeline(
    "text2text-generation",
    model="Falconsai/medical_summarization",
    device_map="auto"
)

@receiver(post_save, sender=MedicalReport)
def auto_summarize_report(sender, instance, created, **kwargs):
    if created and not instance.summary:
        result = summarizer(
            instance.report_text,
            max_new_tokens=150,
            temperature=0.7,
            repetition_penalty=2.0,
            no_repeat_ngram_size=3,
            num_beams=4,
        )[0]
        summary = result.get("generated_text", "").strip()
        instance.summary = summary
        instance.save()
