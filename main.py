import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
sentiment_analysis = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

groserias = ["puto", "puta", "pendejo", "pendeja", "idiota", "imbecil", "estupido", "estupida",
             "mierda", "cabron", "cabrona", "verga", "vergota", "vergudo", "culero", "culera",
             "pendejada", "joto", "mampo", "mampa", "perra", "chinga", "maricon",
             "pendejote", "putazo", "mamon", "mamona"]

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def convertir_calificacion(label):
    calificacion = int(label[0])
    return calificacion

def asignar_etiqueta(score):
    if score <= 2:
        return "Negativo"
    elif score == 3:
        return "Neutro"
    else:
        return "Positivo"

def contiene_groserias(text):
    for palabra in groserias:
        if palabra in text:
            return True
    return False

def analizar_comentario(comentario):
    comentario_procesado = preprocess_text(comentario)
    if contiene_groserias(comentario_procesado):
        return {
            "mensaje": "Tu comentario contiene groserías; por lo tanto no será publicado. Te recomendamos usar un lenguaje adecuado para tu comentario."
        }
    else:
        resultado = sentiment_analysis([comentario_procesado])[0]
        calificacion = convertir_calificacion(resultado['label'])
        etiqueta = asignar_etiqueta(calificacion)
        return {
            "calificacion": calificacion,
        }

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    comentario = data.get('comentario', '')
    resultado = analizar_comentario(comentario)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
