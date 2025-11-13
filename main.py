from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def read_file(filename):
    try:
        with open(filename, "rb") as file:
            binary_content = file.read()
        try:
            content = binary_content.decode('utf-8')
        except UnicodeDecodeError:
            content = binary_content.decode('utf-8', errors='replace')
            print("Some characters were replaced due to encoding issues")
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
    faq = read_file("faq.txt")
    bank_policy = read_file("bank_policy.txt")

    conversation_history = []
    first_interaction = True

    while True:
        if first_interaction:
            user_input = input("What would you like to know about using Wema Bank? Let's have a chat: ").strip()
            first_interaction = False
        else:
            user_input = input("\nWhat else would you like to know? (Type 'exit' to quit): ").strip()

        if user_input.lower() == "exit":
            print("Thank you for banking with us, see you soon!")
            break
        if not user_input:
            print("Mandem, please enter a question")
            continue

        conversation_history.append(user_input)
        
        recent_convo = conversation_history[-3:] if len(conversation_history) > 3 else conversation_history

        if bank_policy is None or faq is None or loan_policy is None:
            print("Could not read one or more policy files. Exiting.")
            return
        
        prompt = f'''
            User Question: {user_input}

            Context:
            - Bank Policies: {bank_policy}
            - Loan Policies: {loan_policy}
            - FAQs: {faq}
            - Recent Conversation: {recent_convo}
            
            Instructions:
            - You are a helpful banking assistant for Wema Bank
            - Answer the user's questions based ONLY on the context provided above: 
                if user asks anything related to banking services/polices, refer to {bank_policy} only.
                if user asks anything related to loans, refer to {loan_policy} only.
                if user asks a question related to general FAQs, refer to {faq} only.
                consider the user's previous question in your subsequent responses.
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
                temperature=0.1,
                max_tokens=1000,
            )

        print(f"\n{response.choices[0].message.content}")

if __name__ == "__main__":
    AI_Assistant()