from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Permitir CORS en todas las rutas

# Configura tu clave API de OpenAI (reemplaza con tu clave API real)
client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")

@app.route('/generate-cv', methods=['POST'])
def generate_cv():
    # Obtener los datos enviados en el cuerpo de la solicitud
    data = request.json
    oferta = data.get('oferta', '')
    experiencia = data.get('experiencia', '')

    # Formatear el mensaje para enviar a OpenAI
    mensaje = f'''
    Dada esta oferta de trabajo: "{oferta}" donde yo tengo esta experiencia: "{experiencia} DEVUELVE SOLO, Y REPITO, SOLO el json para aplicar a la oferta (sin las triple comillas y la palabra json), teniendo en cuenta lo que pide la oferta y lo que sé. no dejes variables vacías, si no tienes la informacion, escribe ej. si es la variable de tlf, pon tu telefono, el estilo del cv tiene que ser exactamente asi: 
    {{
        "personalInfo": {{
            "name": "",
            "location": "",
            "phone": "",
            "email": "",
            "summary": ""
        }},
        "experience": [
            {{
                "id": "",
                "company": "",
                "position": "",
                "location": "",
                "startDate": "",
                "endDate": "",
                "current": false,
                "description": "",
                "bullets": [
                    ""
                ]
            }}
        ],
        "education": [
            {{
                "id": "",
                "institution": "",
                "degree": "",
                "location": "",
                "startDate": "",
                "endDate": "",
                "current": false,
                "description": ""
            }}
        ],
        "skills": [
            ""
        ],
        "themeColor": "",
        "font": ""
    }}
    '''

    try:
        # Realizar la solicitud a la API de OpenAI
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{
                "role": "user",
                "content": mensaje
            }]
        )
        newResponse = response.choices[0].message.content
        # Devolver la respuesta de OpenAI como JSON
        return (newResponse)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
