import requests,time,json
class Chatgbt:
  def __init__(self):
      pass
  def extract_content_from_response(self, response_data):
    try:
        extracted_text = ""
        data_objects = response_data.split("\n\n")
        for data_object in data_objects:
            data = data_object.strip()
            if data.startswith("data:"):
                data = data[5:].strip()
                data_json = json.loads(data)
                choices = data_json.get("choices", [])
                for choice in choices:
                    delta = choice.get("delta", {})
                    if "content" in delta:
                        extracted_text += delta["content"]
        return extracted_text
    except (ValueError, KeyError):
        return ""


  def send_message(self,message):
    url = "https://chat.chatgptdemo.net/chat_api_stream"
    headers = {
      "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
      "Content-Type":"application/json"
    }
    data = {
        "question": f'{message}',
        "timestamp": str(time.time())
    }
    response = requests.post(url,headers=headers,json=data)
    return self.extract_content_from_response(response.text)