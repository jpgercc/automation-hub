# Gmail Email Automation Script

This Python script provides automation for Gmail using the Gmail API. It includes functionality to automatically respond to unread emails from specific senders based on keywords.

## Features

- Authenticate with Gmail API using OAuth2.
- Automatically respond to unread emails from a specified sender if the email body contains all specified keywords.
- Mark the original email as read after sending the automatic response.

## Requirements

- Python 3.x
- Google API Client Libraries:
  - google-auth
  - google-auth-oauthlib
  - google-api-python-client

## Setup

[(API Setup)](https://developers.google.com/workspace/gmail/api/quickstart/python?hl=pt-br)

1. Enable the Gmail API in your Google Cloud Console.
2. Download the `credentials.json` file and place it in the same directory as the script.
3. Install the required Python packages:
   ```
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
4. Run the script. The first time it runs, it will prompt you to authorize access via a browser.

## Usage

- Modify the `remetente_responder`, `palavras_chave_responder`, and `mensagem_resposta_auto` variables in the script to customize the sender, keywords, and automatic reply message.
- Run the script:
  ```
  python main.py
  ```

## Notes

- The script uses the `token.json` file to store and refresh access tokens.

## License

This project is licensed under the MIT License.
