import base64
from openai import OpenAI

def get_api_key(key_file):
    with open(key_file, 'r') as file:
        api_key = file.readline().strip()
    
    return api_key


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

def gpt_analysis(image_path, provided_url, visited_url):
    api_key = get_api_key("api_key.txt")
    client = OpenAI(api_key=api_key)
    encoded_image = encode_image_to_base64(image_path)

    system_prompt = "You are an expert at analyzing webpage screenshots(images) and webpage urls for phishing webpage detection."
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt},
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Provided URL: {provided_url}"},
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Visited URL: {visited_url}"},
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "From the provided webpage screenshot and url, you are able to determine whether the webpage under examination is a phishing site or not. As you determine whether the webpage is phishing, do also identify the target brand, any user credential fields, the phishing indicators. Provide your response in the following format: 1. Target Brand, 2. Has user credential fields (i.e Yes/No) 3. (List of) Phishing Indicators, 4. Conclusion (i.e Phishing/Non-phishing)."},
                ],
            },
        ],
        max_tokens=1000,
    )

    # Prints the content of the response received from the GPT model
    print(response.choices[0].message.content)

    # Prints information about the usage of the model
    print(response.usage.model_dump())


gpt_analysis("screenshot_aft.png", "https://itachi2704.github.io/netflix-clone/", "https://itachi2704.github.io/netflix-clone/")