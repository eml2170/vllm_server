from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer


app = Flask(__name__)
model_name = "BioMistral/BioMistral-7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    clinical_note = data["clinical_note"]
    prompt = f"Extract the diagnoses from the following clinical note:\n{clinical_note}\n\nDiagnoses:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)

    # Prepare the output schema.
    diagnoses = []
    for dx in outputs[0].text.split():
        diagnoses.append(dx)
    result = {
        "diagnoses": diagnoses
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)