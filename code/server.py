from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

from prompts import ZEROSHOT_PROMPT
from utils import create_logger

logger = create_logger()
app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")
logger.info("Loaded model")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        logger.debug(f"Received request: {data}")
        clinical_note = data["clinical_note"]

        prompt = ZEROSHOT_PROMPT.format(clinical_note=clinical_note)

        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            # do_sample=True,
            # temperature=0.1,
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.debug(f"Raw response: {generated_text}")

        # Extract the diagnoses part
        diagnoses_text = generated_text.split("Diagnoses (supported by symptoms):")[
            -1
        ].strip()

        # Post-processing
        diagnoses = []
        for dx in diagnoses_text.replace(";", "\n").split("\n"):
            dx = dx.strip()
            # Remove numbering, bullets, and other artifacts
            dx = dx.lstrip("0123456789.-• ").strip()
            # Only add non-empty, unique diagnoses
            if dx and dx not in diagnoses:
                diagnoses.append(dx)

        return jsonify(
            {
                "diagnoses": diagnoses,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
