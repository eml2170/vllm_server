ZEROSHOT_PROMPT = """Given the following clinical note, list only the diagnoses mentioned and explicitly supported by the note. Do not include speculative diagnoses. There may be 0 diagnoses. List each diagnosis on a new line without numbers, letters or bullets.

Clinical note:
{clinical_note}

Diagnoses:"""
