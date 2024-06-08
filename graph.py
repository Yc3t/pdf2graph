import os
import fitz
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.
api_key = os.getenv("GOOGLE_API_KEY")
def Gemini(prompt, file_text):
    genai.configure(api_key=api_key)

    # Create the model

    generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 592,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
    )

    response = model.generate_content([prompt,file_text], stream = True)
    
    for chunk in response:
        print(chunk.text)
        
    generated_text = ""
    for chunk in response:
        generated_text += chunk.text

    return generated_text


def read_pdf(pdf_path):

    pdf_doc = fitz.open(pdf_path)

    full_text = ""

    for page_num in range(len(pdf_doc)):

        page = pdf_doc[page_num]
        text = page.get_text("text")

        full_text += text + "\n"

    return full_text

def modify_html(structure, html_file_path):
    with open(html_file_path, 'r') as file:
        filedata = file.read()

    # Find the start and end of the existing structure
    start = filedata.find('const structure = `')
    end = filedata.find('`;', start) + len('`;')

    # Replace the existing structure with the new one
    filedata = filedata[:start] + 'const structure = `' + structure + '`;' + filedata[end:]

    # Write the file out again
    with open(html_file_path, 'w') as file:
        file.write(filedata)

def main():

    prompt = """Please analyze the provided PDF document and generate a structured outline based on its content. The structure should include main topics, subtopics, and detailed points under each subtopic using the bracket notation Use as many points as necessary. Follow the format below:

        **Format:**
        ```
        <Title> Main Topic </Title>
        - <Topic 1> Subtopic </Topic 1>
        - <Subtopic 1-1> Detailed Point </Subtopic 1-1>
            - <Subtopic 1-1-1> Description of the point. </Subtopic 1-1-1>
            - <Subtopic 1-1-2> Description of the point. </Subtopic 1-1-2>
        - <Subtopic 1-2> Detailed Point </Subtopic 1-2>
            - <Subtopic 1-2-1> Description of the point. </Subtopic 1-2-1>
            - <Subtopic 1-2-2> Description of the point. </Subtopic 1-2-2>
        - <Topic 2> Subtopic </Topic 2>
        - <Subtopic 2-1> Detailed Point </Subtopic 2-1>
            - <Subtopic 2-1-1> Description of the point. </Subtopic 2-1-1>
            - <Subtopic 2-1-2> Description of the point. </Subtopic 2-1-2>
        ```

        **Example:**
        ```
        <Title> Technique of Psychoanalytic Therapy </Title>
        - <Topic 1> Basic Rule of Psychoanalysis </Topic 1>
        - <Subtopic 1-1> The analyst helps the patient make the unconscious conscious through the interpretation of unconscious material. </Subtopic 1-1>
            - <Subtopic 1-1-1> The basic rule requires the abolishment of the censor and allowing thoughts to associate freely. </Subtopic 1-1-1>
            - <Subtopic 1-1-2> The basic rule is opposed by the counter-cathexis of the ego, which leads to resistance. </Subtopic 1-1-2>
        - <Topic 2> The Role of Resistance Analysis </Topic 2>
        - <Subtopic 2-1> The analyst must understand and interpret resistances, which are the result of the ego's efforts to defend itself against the repressed material. </Subtopic 2>
        """

    pdf_file = "example.pdf"

    text_data = read_pdf(pdf_file)
    
    structure = Gemini(prompt, text_data)
    modify_html(structure, 'templates/index.html')




if __name__ == "__main__":
    main()





