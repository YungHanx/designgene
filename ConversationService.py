import requests
import json

class ConversationService():
    url = "https://xxxxxxxxxxxx"
    headers = {
        "Ocp-Apim-Subscription-Key": "xxxxxxxxxx",
        "Apim-Request-Id": "xxxxxxxxxx",
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "text": "",
                "modality": "text",
                "language": "en-us",
                "participantId": "1"
            }
        },
        "parameters": {
            "projectName": "dgmodel",
            "verbose": True,
            "deploymentName": "dg3",
            "stringIndexType": "TextElement_V8"
        }
    }
    ENTITIES = []
    def __init__(self):
        self.LUIS_RESPONSE = None
    def getConversationResponse(self, message):
        self.payload["analysisInput"]["conversationItem"]["text"] = message
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.payload))
        if response.status_code == 200:
            self.LUIS_RESPONSE = response.json()
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    def getTopIntent(self):
        if self.LUIS_RESPONSE:
            return self.LUIS_RESPONSE['result']['prediction']['topIntent']
        else:
            print("Error LUIS RESPONSE is not defined")
            return None
    def getEntities(self):
        design_entities = ["Round", "Triangle", "Square", "Spiral", "Morden", "Contemporary", "Crisp", "Vibrant", "Light", "Warm", "Rich", "Refine", "Spirt"]
        if self.LUIS_RESPONSE:
            result = []
            entities = self.LUIS_RESPONSE['result']['prediction']['entities']
            if entities:
                for entity in entities:
                    if entity['category'] in design_entities:
                        self.ENTITIES.append('Design_Style')
                        result.append({
                            "Design_Style":[
                                {
                                "name": entity['category'],
                                "value": entity['text'],
                                "confidence": entity['confidenceScore']
                            }
                            ]
                            })
                    else: 
                        self.ENTITIES.append(entity['category'])
                        result.append({
                            entity['category']: [
                                {
                                "name": entity['category'],
                                "value": entity['text'],
                                "confidence": entity['confidenceScore']
                                }
                            ]
                            })
                return result
            else:
                print("Error LUIS RESPONSE has no entities")
                return []
        else:
            print("Error LUIS RESPONSE is not defined")
            return []
    def genNewTag(self, old_tag, new_tag):#第三題
        combined_list = []
        combined_list.extend(old_tag)
        for item in new_tag:
            found = False
            for a_item in combined_list:
                if a_item == item:
                    found = True
                    break
            if not found:
                combined_list.append(item)
        return combined_list
    
