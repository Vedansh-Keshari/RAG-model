import google.generativeai as genai

genai.configure(api_key="AIzaSyBCT9eKXaYEmKypGEv-B6OWWkCzP-kEXbM")

# List available models
for model in genai.list_models():
    print(model.name)