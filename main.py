from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# def read_bank_policies():
#     try:
#         with open("group_bank_policies.txt", "rb") as file:
#             binary_content = file.read()
            
#         try:
#             content = binary_content.decode('utf-8')
#         except UnicodeDecodeError:
                
#             content = binary_content.decode('utf-8', errors='replace')
#             print("Some characters were replaced due to encoding issues")
            
#         print(f"File read successfully ({len(content)} characters)")
#         return content
            
#     except FileNotFoundError:
#         print("Error: group_bank_policies.txt file not found!")
#         return None
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return None

def read_file(filename):
    try:
        with open(filename, "rb") as file:
            binary_content = file.read()
        try:
            content = binary_content.decode('utf-8')
        except UnicodeDecodeError:
            content = binary_content.decode('utf-8', errors='replace')
            print("Some characters were replaced due to encoding issues")
        print(f"File '{filename}' read successfully ({len(content)} characters)")
        return content
    except FileNotFoundError:
        print(f"Error: {filename} file not found!")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def AI_Assistant():
    assistant = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint="https://ugoch-mhrmec5e-eastus2.cognitiveservices.azure.com/",
        api_key=os.getenv("API_KEY"),
    )

    loan_policy = read_file("loan_policy.txt")
    faQ = read_file("faq.txt")
    bank_policy = read_file("bank_policy.txt")

    if bank_policy is None or faQ is None or loan_policy is None:
        print("Could not read one or more policy files. Exiting.")
        return

    user_input = input("What would you like to know about using Wema Bank? Let's have a chat :): ")

    prompt = f'''
        User Question: {user_input}

        Context: {bank_policy, faQ, loan_policy}
        
        Instructions:
        - You are a helpful banking assistant for Wema Bank
        - Answer the user's questions based ONLY on the context provided above: 
            if user asks anything related to banking services/polices, refer to {bank_policy} only.
            if user asks anything related to loans, refer to {loan_policy} only.
            if user asks a question related to general FAQs, refer to {faQ} only.
        - Do not go beyond the scope of this context
        - Do not hallucinate or make up information
        - If the user asks something outside the context, politely inform them that you can only answer questions related to Wema Bank services
        - Always begin your responses by addressing the user as "Mandem"
        - Keep responses clear and helpful. Emojis are always welcome.
    '''

    response = assistant.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful banking assistant for Wema Bank. "
                "Always address users as 'Mandem' and be polite."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=5000,
        )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    AI_Assistant()