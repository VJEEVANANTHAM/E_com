from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-3.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)