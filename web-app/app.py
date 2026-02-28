from flask import Flask, render_template, request, Response, jsonify
from ollama import chat
import json
import hashlib
from datetime import datetime
import boto3
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('principal.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/vision-page')
def vision_page():
    return render_template('vision_page.html')

@app.route('/cloud')
def cloud():
    return render_template('cloud.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/prompt', methods=['POST'])
def api_prompt():
    prompt = request.json.get('prompt', '')
    
    response = chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    datahora = datetime.now().isoformat()
    hash_id = hashlib.sha256(f"{prompt}{datahora}".encode()).hexdigest()
    
    return jsonify({
        "resposta": response['message']['content'],
        "datahora": datahora,
        "id": hash_id
    })

@app.route('/cloud/bedrock', methods=['POST'])
def cloud_bedrock():
    prompt = request.json.get('prompt', '')
    
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        body = json.dumps({
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 512, "temperature": 0.7}
        })
        
        response = bedrock.invoke_model(
            modelId='us.amazon.nova-lite-v1:0',
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        return jsonify({"response": response_body['output']['message']['content'][0]['text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cloud/canvas', methods=['POST'])
def cloud_canvas():
    prompt = request.json.get('prompt', '')
    
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "width": 512,
                "height": 512
            }
        })
        
        response = bedrock.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        image_base64 = response_body['images'][0]
        return jsonify({"image": image_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    user_query = 'Responda de forma resumida, com no máximo 100 palavras: ' + request.json.get('message', '')

    def generate():
        stream = chat(
            model='gemma3',
            messages=[{'role': 'user', 'content': user_query}],
            stream=True,
        )
        for chunk in stream:
            yield f"data: {json.dumps({'content': chunk['message']['content']})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/vision', methods=['POST'])
def vision():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400
    
    file = request.files['image']
    image_bytes = file.read()
    print("Iniciando analise")
    
    response = chat(
        model='gemma3',
        messages=[{
            'role': 'user',
            'content': 'Responda de forma resumida, com no máximo 100 palavras: Descreva esta imagem em detalhes, por favor.',
            'images': [image_bytes]
        }]
    )
    
    print("Analise concluida")
    return jsonify({"description": response['message']['content']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
