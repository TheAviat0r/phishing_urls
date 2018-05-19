# PhishCracker Telegram Bot

Telegram bot for detecting phishing urls in group chats.

## Requirements
1. Installed Docker.
2. Available and working VPN (for Russian users).
3. Registered Telegram bot, which was added in target chats.

## Installation
1. Copy your bot access token and save it in 'tgtoken' file, which
   should be in the same directory as Dockerfile
2. Build Docker image.
```
docker buid -t <image_name> .
```
3. Add your bot to your target chat.
4. docker run -d -e nworkers=<number of workers required> <container>

