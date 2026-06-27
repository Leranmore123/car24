import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from cars.models import InspectionReport

def clean_notes():
    reports = InspectionReport.objects.all()
    count = 0
    for r in reports:
        if r.inspector_notes and ("commission" in r.inspector_notes.lower()):
            # Replace the commission text entirely with a standard certified note
            cleaned = re.sub(
                r"Commission set at:.*", 
                "Checked and certified by CarBazaar. Excellent overall condition with fully functional components.", 
                r.inspector_notes,
                flags=re.IGNORECASE
            )
            # Remove any trailing "Checked by CarBazaar." parts to keep it clean
            cleaned = cleaned.replace("Commission set at: ", "").strip()
            # If the notes end up empty or just contain the commission part, replace it fully
            if not cleaned or "commission" in cleaned.lower():
                cleaned = "Evaluation successfully passed. Checked and certified by CarBazaar. Excellent overall condition with fully functional components."
            
            r.inspector_notes = cleaned
            r.save()
            count += 1
            print(f"Cleaned inspection notes for Report ID {r.id}: {r.inspector_notes}")
            
    print(f"Successfully updated {count} inspection reports.")

if __name__ == "__main__":
    clean_notes()
