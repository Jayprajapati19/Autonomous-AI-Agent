# main.py
from agent import ask_llm
from tools.search_tool import search_web
from tools.summarize_tool import summarize_text
from tools.email_tool import send_email
# from tools.launcher_tool import open_file
import re  # moved to top for consistency

def menu():
    print("\n=== AI Task Assistant ===")
    print("1. Ask AI anything")
    print("2. Search the web")
    print("3. Summarize text")
    print("4. Send email")
    print("5. Open file/app")
    print("6. Smart email assistant")
    print("0. Exit")

def main():
    while True:
        menu()
        choice = input("\nChoose an option: ")

        if choice == "1":
            prompt = input("Ask: ")
            print(ask_llm(prompt))

        elif choice == "2":
            q = input("Search for: ")
            results = search_web(q)
            print(results)
           

        elif choice == "3":
            text = input("Enter text to summarize: ")
            print(summarize_text(text))

        elif choice == "4":
            subject = input("Subject: ")
            body = input("Body: ")
            to = input("To email: ")
            from_email = input("Your Gmail: ")
            password = input("Your App Password: ")
            print(send_email(subject, body, to, from_email, password))

        elif choice == "5":
            file_prompt = input("Which file to open (you can just say its name): ")
            if file_prompt.lower().startswith("open "):
                file_name = file_prompt[5:].strip()
            
            else:
                file_name = file_prompt
            
            from tools.launcher_tool import open_file_by_name
            print(open_file_by_name(file_name))
           
            
            

        elif choice == "6":
            raw_prompt = input("Describe the email task (e.g., 'write email to john@example.com about project delay'): ")

            # Extract email from prompt
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', raw_prompt)
            if not email_match:
                print("❌ Could not find an email address in your prompt.")
                continue

            to_email = email_match.group(0)

            # Remove email and common keywords from prompt
            task_desc = raw_prompt.replace(to_email, "").replace("email", "").replace("to", "").strip()

            if not task_desc:
                print("❌ Couldn't understand the prompt. Use: 'write email to someone@example.com about ...'")
                continue

            # Generate email body and subject
            body_prompt = (
                f"Write the body of a professional but friendly email about: {task_desc}. "
                "Do not include the subject line. Address the recipient directly without placeholders. "
                "Keep it concise and natural."
            )

            subject_prompt = (
                f"Generate only one short, professional subject line for an email about: {task_desc}. "
                "Do not include multiple options or extra text."
            )

            email_body = ask_llm(body_prompt)
            email_subject = ask_llm(subject_prompt)

            # Send email (assuming credentials are handled inside send_email or via env)
            print(send_email(email_subject, email_body, to_email))

        elif choice == "0":
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
