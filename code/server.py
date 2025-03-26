from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer


app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        clinical_note = data["clinical_note"]
        prompt = f"Extract the diagnoses from the following clinical note:\n{clinical_note}\n\nDiagnoses:"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the diagnoses part
        diagnoses_text = generated_text.split("Diagnoses:")[-1].strip()
        
        # Split on newlines, commas, or semicolons
        diagnoses = [dx.strip() for dx in diagnoses_text.replace(";", "\n").replace(",", "\n").split("\n") if dx.strip()]
        
        return jsonify({
            "diagnoses": diagnoses
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)