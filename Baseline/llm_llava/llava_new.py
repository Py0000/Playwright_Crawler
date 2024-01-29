from transformers import LlavaForConditionalGeneration, AutoProcessor
from PIL import Image
import argparse
import json
import os
import shutil
import zipfile

def generate_response_helper(model, processor, image_path, provided_url, visited_url):
    # Structuring the prompts
    system_prompt = "You are an expert at analyzing webpage screenshots(images) and webpage urls for phishing webpage detection."
    urls = f"Provided_Url: {provided_url}. Visited_Url: {visited_url}"
    response_format_prompt = "From the provided webpage screenshot and url, you are able to determine whether the webpage under examination is a phishing site or not. As you determine whether the webpage is phishing, do also identify the target brand, any user credential fields, the phishing indicators. Provide your response in the following format: 1. Target Brand, 2. Has user credential fields (i.e Yes/No) 3. (List of) Phishing Indicators, 4. Conclusion (i.e Phishing/Non-phishing)."
    full_prompt = f"<image>\nUSER:{system_prompt}\n{urls}\n{response_format_prompt}\nASSISTANT:"
    image = Image.open(image_path)

    inputs = processor(text=full_prompt, images=image, return_tensors="pt")

    # Generate output
    generate_ids = model.generate(**inputs, max_length=5000)
    output = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return output

def generate_response(image_path, provided_url, visited_url):
    # Load the model and tokenizer 
    model = LlavaForConditionalGeneration.from_pretrained("llava-hf/bakLlava-v1-hf")
    processor = AutoProcessor.from_pretrained("llava-hf/bakLlava-v1-hf")

    return generate_response_helper(model, processor, image_path, provided_url, visited_url)


def process_directory(zip_folder_path, benign_phishing):
    responses = []

    for zip_file in os.listdir(zip_folder_path):
        print(f"Processing {zip_file}")
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(zip_folder_path, zip_file)

            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extract_path = os.path.join(zip_folder_path, zip_file.replace('.zip', ''))
                zip_ref.extractall(extract_path)
                if benign_phishing == "phishing":
                    self_ref_path = os.path.join(extract_path, extract_path.split("/")[1], 'self_ref')
                else:
                    self_ref_path = os.path.join(extract_path, 'self_ref')

                if os.path.exists(self_ref_path):
                    screenshot_path = os.path.join(self_ref_path, 'screenshot_aft.png')
                    log_path = os.path.join(self_ref_path, 'log.json')

                    if not os.path.exists(screenshot_path) or not os.path.exists(log_path):
                        responses.append("Error due to missing file(s).")
                        continue

                    with open(log_path, 'r') as log_file:
                        log_data = json.load(log_file)
                        provided_url = log_data.get("Provided Url", "")
                        visited_url = log_data.get("Url visited", "")
                    
                    resp = generate_response(screenshot_path, provided_url, visited_url)
                    responses.append(resp)
                
                # Delete the extracted folder after processing
                shutil.rmtree(extract_path)
                
    date = zip_folder_path.split("_")[-1]
    output_file = f"llava_analysis_{date}.txt"
    with open(output_file, 'w') as file:
        for response in responses:
            file.write(response + "\n\n\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("folder_path", help="Folder name")
    parser.add_argument("benign_phishing", help="benign or phishing")
    args = parser.parse_args()

    folder_name = args.folder_path 
    process_directory(folder_name, args.benign_phishing)