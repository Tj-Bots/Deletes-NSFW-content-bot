# 🛡️ NSFW Guard Bot (AI Deep Learning Filter)

A powerful, real-time NSFW content filter for Telegram groups and channels. This bot uses a deep learning model (**MobileNetV2**) to analyze images, videos, GIFs, and animations.

---

## 🚀 Features
- **Real-time AI Scanning:** Automatically detects and removes inappropriate content.
- **Deep Learning Accuracy:** Categorizes content into: `porn`, `hentai`, `sexy`, `drawings`, and `neutral`.
- **Easy Setup:** Works instantly in any group or channel after being added as an admin.
- **Privacy-Focused:** Images are analyzed locally (or on your server) and deleted immediately after processing.

---

## 🛠️ Installation & Setup

### 1. Requirements
- Python 3.9 or higher.
- `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
- `BOT_TOKEN` from [@BotFather](https://t.me/BotFather).

### 2. Manual Deployment (VPS/Local)
```bash
# Clone the repository
git clone https://github.com/Tj-Bots/Deletes-NSFW-content-bot
cd Deletes-NSFW-content-bot

# Install dependencies
pip install -r requirements.txt

# Set Environment Variables
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export ADMIN_ID="your_user_id"

# Run the bot
python3 bot.py
```

### 3. Docker Deployment
```bash
docker build -t nsfw-guard-bot .
docker run -d \
  -e API_ID="your_api_id" \
  -e API_HASH="your_api_hash" \
  -e BOT_TOKEN="your_bot_token" \
  -e ADMIN_ID="your_user_id" \
  nsfw-guard-bot
```

### 4. Heroku Deployment
1. Click the **Deploy to Heroku** button (if added) or:
2. Create a new app.
3. Add the following **Config Vars**:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `ADMIN_ID`
4. Deploy the repository.

---

## 📊 Detection Categories & Thresholds
The bot uses a classification system with the following categories:
- **Porn:** Explicit adult content (Photos/Videos).
- **Hentai:** Explicit anime/cartoon content.
- **Sexy:** Suggestive but not explicit (Swimsuits, modeling).
- **Drawings:** Safe-for-work anime/cartoon content.
- **Neutral:** Safe-for-work general content.

By default, the bot removes content with a score > 0.90 in `Porn`, `Hentai`, or `Sexy`. You can adjust these thresholds in `bot.py`.

---

## 👨‍💻 Author
Created by **Boss** & **Lexy**.
GitHub: [Tj-Bots](https://github.com/Tj-Bots)

---

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
