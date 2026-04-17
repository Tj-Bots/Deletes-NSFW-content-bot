import os
import logging
import asyncio
import numpy as np
from PIL import Image
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import tensorflow as tf
import tensorflow_hub as hub
import tf_keras

# --- Configuration (from Environment Variables for Security) ---
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0')) # Optional: Admin for special commands

# Paths
MODEL_PATH = 'nsfw_mobilenet2.h5'
DOWNLOADS_DIR = 'downloads'

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Categories from the model
CATEGORIES = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# --- Model Loading ---
logger.info("Loading NSFW model...")
try:
    model = tf_keras.models.load_model(
        MODEL_PATH,
        custom_objects={'KerasLayer': hub.KerasLayer}
    )
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    # If model is missing, we try to download it or stop
    exit(1)

def predict_nsfw(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = model.predict(img_array, verbose=0)[0]
        results = dict(zip(CATEGORIES, [float(p) for p in predictions]))
        
        # NSFW logic: You can adjust these thresholds
        is_bad = (
            results['porn'] > 0.90 or 
            results['hentai'] > 0.90 or 
            results['sexy'] > 0.90
        )
        
        return is_bad, results
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return False, {}

# --- Bot Client ---
app = Client("nsfw_guard_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    text = (
        "🛡️ **Welcome to NSFW Guard Bot**\n\n"
        "I automatically scan and remove NSFW content (pornography, hentai) from this chat.\n\n"
        "🔹 **How it works:** I use a deep learning model (MobileNetV2) to analyze images and videos in real-time.\n"
        "🔹 **Setup:** Just add me as an Admin with delete permissions."
    )
    await message.reply(text)

@app.on_message((filters.photo | filters.video | filters.document | filters.animation))
async def monitor_content(client, message: Message):
    # Process only in groups/channels or if authorized
    file_id = None
    media = message.photo or message.video or message.animation or message.document
    
    if not media: return

    if message.photo:
        file_id = message.photo.file_id
    elif hasattr(media, "thumbs") and media.thumbs:
        file_id = media.thumbs[-1].file_id
    elif message.document and "image" in (message.document.mime_type or ""):
        file_id = message.document.file_id

    if not file_id: return

    try:
        file_path = await client.download_media(file_id, file_name=os.path.join(DOWNLOADS_DIR, f"{file_id}.jpg"))
        if not file_path: return

        is_bad, scores = predict_nsfw(file_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        if is_bad:
            logger.info(f"NSFW Detected in {message.chat.id}: {scores}")
            
            # Format scores
            formatted_scores = "\n".join([f"• **{k.capitalize()}**: `{v:.2f}`" for k, v in scores.items()])
            
            try:
                await client.send_message(
                    message.chat.id, 
                    f"⚠️ **Inappropriate Content Removed**\n\n"
                    f"🔞 This message was automatically removed by AI filter.\n"
                    f"📊 **Detection Scores:**\n{formatted_scores}"
                )
            except:
                pass
            
            await message.delete()
                
    except Exception as e:
        logger.error(f"Monitoring error: {e}")

if __name__ == "__main__":
    logger.info("Bot is starting...")
    app.run()
