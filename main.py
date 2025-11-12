from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def AI_Assistant():
    assistant = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint="https://ugoch-mhrmec5e-eastus2.cognitiveservices.azure.com/",
        api_key=os.getenv("API_KEY"),
    )

    user_input = input("What would you like to know? Ask Here: ")

    prompt = f'''
        User Question: {user_input}
        
        Context: {bank_policies}
        
        Instructions:
        - You are a helpful banking FAQ assistant for Wema Bank
        - Answer the user's questions based ONLY on the context provided above
        - Do not go beyond the scope of this context
        - Do not hallucinate or make up information
        - If the user asks something outside the context, politely inform them that you can only answer questions related to Wema Bank services
        - Always begin your responses by addressing the user as "Mandem"
        - Keep responses clear and helpful
    '''

    response = assistant.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a helpful banking FAQ assistant for Wema Bank. "
                "Always address users as 'Mandem' and be polite. Context: {bank_policies}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1000,
        )

    print("AI Assistant Response:", response.choices[0].message.content)

if __name__ == "__main__":
    AI_Assistant()