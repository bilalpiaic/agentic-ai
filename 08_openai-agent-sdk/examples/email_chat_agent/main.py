from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import mimetypes

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')
email_address = os.getenv('EMAIL_ADDRESS')
app_password = os.getenv('EMAIL_APP_PASSWORD')
imap_server = "imap.gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

sys_prompt = """
You are a smart and professional Email Agent. Your primary role is to manage and interact with the user's email using two main capabilities: reading and sending emails. You act on behalf of the user to understand, summarize, respond to, and manage emails across different use cases — from general correspondence to task delegation and follow-ups.

### 🧠 **General Capabilities**

1. **Email Comprehension**:

   * Extract and summarize key details: sender, subject, intent, requests, deadlines.
   * Detect tone (e.g., urgent, casual, angry, formal).
   * Recognize email threads and ongoing conversations.

2. **Smart Reply Drafting**:

   * Generate well-formatted, grammatically correct, contextually relevant replies.
   * Maintain tone consistency (e.g., professional, friendly, assertive) based on sender's tone and user's preference.
   * Ask for clarification only if absolutely necessary.

3. **Inbox Management**:

   * Prioritize and categorize emails (e.g., urgent, follow-up, informational).
   * Detect spammy or suspicious emails.
   * Track unresolved action items and follow-ups.

4. **Email Writing Assistance**:

   * Compose new emails from user instructions with high professionalism and structure.
   * Handle attachments properly when sending emails.

---

### 🛠️ **Tool Usage Instructions**

You can access two tools to perform actions:

#### 1. `read_emails(folder="INBOX", days=7, max_emails=10)`

Use this tool to fetch recent emails from the user's inbox (or other folders like "Spam"). You should:

* Read only the number of emails needed for the task.
* Choose the appropriate folder (default: "INBOX").
* Avoid fetching unnecessary messages — always use the minimal value of `max_emails` for efficiency.
* Parse the subject, sender, and body of the email to help the user quickly understand its purpose.

**Example use cases**:

* "Check unread emails from this week."
* "Read emails from the Spam folder."
* "Summarize my last 5 emails."

#### 2. `send_email(recipient_email, subject, body, attachments=[])`

Use this tool to send emails on behalf of the user. You must:

* Ensure the subject and body are clearly written.
* Include all necessary information in the email body.
* Attach files only if explicitly instructed or required by context.
* Maintain formatting and clarity.

**Example use cases**:

* "Reply to the recruiter with my availability."
* "Send a follow-up email to the client with the project report attached."

---

### ✅ **Best Practices**

* **Be proactive**: Suggest useful follow-ups or replies if emails imply pending tasks or unclear conclusions.
* **Be discreet and secure**: Do not expose sensitive data unnecessarily. Handle passwords, addresses, and attachments responsibly.
* **Be efficient**: Don’t read or send more emails than required. Optimize API calls by using relevant filters and limits.

---

### ⚠️ **Constraints**

* Do not hallucinate email content. Only respond based on actual fetched email data.
* Do not assume context across unrelated emails unless they form a thread.
* Never attempt to execute outside commands not related to email operations.
* Never use tools for non-email-related tasks.

---

### 🧾 **Example Scenarios**

* **User**: “Summarize the most important emails I received this week.”
  → Use `read_emails(days=7, max_emails=10)`, extract key topics, and summarize.

* **User**: “Reply to John saying I’ll join the meeting at 3 PM.”
  → Fetch recent emails from John, draft a contextual reply, and use `send_email`.

* **User**: “Send an email to [hr@example.com](mailto:hr@example.com) with subject ‘Leave Request’ and body ‘I’d like to apply for leave from June 10 to June 15.’”
  → Use `send_email` directly with the provided info.

---

### 🎯 **Objective**

Make the user’s email experience fast, clear, and intelligent. Reduce manual work. Help them focus on decision-making instead of inbox processing.

"""

@function_tool
def read_emails(
    folder: str = "INBOX",
    days: int = 7,
    max_emails: int = 10
):
    """
    Read emails using IMAP.
    
    Parameters:
    - email_address: your email address
    - app_password: app-specific password or actual password (if allowed)
    - imap_server: IMAP server, e.g., imap.gmail.com
    - folder: Mailbox folder, e.g., INBOX, Spam
    - days: Number of past days to fetch emails from
    - max_emails: Maximum number of emails to fetch
    """
    try:
        # Connect and login
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, app_password)

        # Select the folder
        imap.select(folder)

        # Compute date N days ago
        date_since = (datetime.now() - timedelta(days=days)).strftime('%d-%b-%Y')

        # Search emails since the given date
        status, messages = imap.search(None, f'(SINCE "{date_since}")')
        if status != "OK":
            print("Error searching emails")
            return []

        email_ids = messages[0].split()
        email_ids = email_ids[-max_emails:]  # Limit to most recent `max_emails`
        emails = []

        for eid in reversed(email_ids):
            status, msg_data = imap.fetch(eid, "(RFC822)")
            for part in msg_data:
                if isinstance(part, tuple):
                    msg = email.message_from_bytes(part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                    from_ = msg.get("From")

                    body = ""
                    if msg.is_multipart():
                        for subpart in msg.walk():
                            if subpart.get_content_type() == "text/plain" and "attachment" not in str(subpart.get("Content-Disposition")):
                                body = subpart.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    emails.append({
                        "from": from_,
                        "subject": subject,
                        "body": body.strip()[:500],  # Truncate to first 500 chars
                    })
        
        imap.logout()
        return emails
    
    except Exception as e:
        print("Error:", e)
        return []

@function_tool
def send_email(
    recipient_email: str,
    subject: str,
    body: str,
    attachments: list = []
):
    """
    Send an email with optional attachments using SMTP.

    Parameters:
    - email_address: Your email address
    - app_password: App password or real password
    - recipient_email: Receiver's email
    - subject: Email subject
    - body: Email body (plain text)
    - smtp_server: SMTP server (default: Gmail)
    - smtp_port: SMTP port (default: 587)
    - attachments: List of file paths to attach
    """
    try:
        msg = EmailMessage()
        msg["From"] = email_address
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Attach files
        if attachments:
            for filepath in attachments:
                if os.path.isfile(filepath):
                    mime_type, _ = mimetypes.guess_type(filepath)
                    mime_type, mime_subtype = (mime_type or "application/octet-stream").split("/")
                    with open(filepath, "rb") as f:
                        file_data = f.read()
                        file_name = os.path.basename(filepath)
                        msg.add_attachment(
                            file_data,
                            maintype=mime_type,
                            subtype=mime_subtype,
                            filename=file_name
                        )

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, app_password)
            server.send_message(msg)
        
        print("✅ Email sent successfully.")
        return True

    except Exception as e:
        print("❌ Error sending email:", e)
        return False



agent = Agent(
    name="Email Assistant",
    instructions=sys_prompt,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[read_emails, send_email]
)
history = []

while True:

    query = input("Enter the query: ")

    history.append({"role": "user", "content": query})

    result = Runner.run_sync(
        agent,
        history,
    )

    li = result.to_input_list()
    
    history.extend(li)

    print(result.final_output)