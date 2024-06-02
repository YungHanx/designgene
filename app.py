from flask import Flask, abort, request
from flask_restx import Resource, Api, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv
import json
from RecommendationServiceBot import RecommendationServiceBot
import uuid

BASE_URL = "api"

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, version='1.0', 
    title='AI API',
    description='A AI Tool created with OpenAI GPT-3.5',
    doc='/' + BASE_URL + '/docs/'
)
load_dotenv()
ns = api.namespace(BASE_URL, description='AI API')

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
chat_payload = api.model('chat', {
    'user_id': fields.String,
    'message': fields.String,
})

chat_res = api.model('chat_res', {
    'user_id': fields.String,
    'question': fields.String,
    'status': fields.String, # pending, success, failed
    'tags': fields.Raw(example=[
        {
            "name": "Abstract",
            "confidence": 0.8
        }
    ]),
})

@ns.route('/chat/callback')
class LineBot(Resource):
    @api.expect(chat_payload)
    @api.marshal_with(chat_res)
    def post(self):
        # get request body as text
        body = request.get_data(as_text=True)#向客戶端請求他們的訊息
        app.logger.info("Request body: " + body)
        body = json.loads(body)
        user_id = body.get('user_id')#生成一個變數
        if user_id == "":
            user_id = str(uuid.uuid4())
        message = body.get('message')
        BOT = RecommendationServiceBot(user_id, message)
        response = BOT.getReply()
        # get response from AI
        return response
    

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")

mock_response = {
          "user_id": "123",
          "question": "Can you introduce yourself? The purpose is to let me know you well? For example: Tell me what is your Brand name? What is your industry? Or your company's goals and vision?",
          "status": "Pending",
          "tags": [
            {
              "entity": "Brand_Name",
              "value": "ArtisticEdge Design Co",
              "confidence": 0.8
            },
            {
              "entity": "Brand_Product",
              "value": "boutique design firm",
              "confidence": 0.9
            },
            {
              "entity": "Brand_Goal",
              "value": "elevate brands through bespoke design solutions that capture the essence of their story and connect with their audience on a deeper level.",
              "confidence": 0.7
            }
          ]
        }