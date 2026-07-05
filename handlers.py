import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import database
import banner_generator
import image_utils
import keyboards

BRAND, PLATFORM, STYLE, COLORS, DESCRIPTION = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_utils.ensure_temp_directory()
    uid = update.effective_user.id
    await database.register_user(uid)
    
    welcome = (
        "👋 Welcome to *BannerCraft Bot*!\n"
        "Create stunning AI-powered banners for your social media profiles, websites, and brands.\n\n"
        "🎨 *Generate professional banners instantly*\n"
        "📱 *Optimized layouts for YouTube, LinkedIn, X, and Facebook*\n"
        "🖼 *Powered by premium generative imaging layers*\n\n"
        "Choose an option below or start creating your first banner."
    )
    if update.message:
        await update.message.reply_text(welcome, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
    return ConversationHandler.END

async def start_creation_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["banner_data"] = {}
    await query.message.reply_text("🚀 Let's begin! What is your *Brand Name* or primary text header?", parse_mode="Markdown")
    return BRAND

async def get_brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["banner_data"]["brand"] = update.message.text
    kb = [[InlineKeyboardButton("YouTube Art", callback_data="plt_YouTube")],
          [InlineKeyboardButton("LinkedIn Banner", callback_data="plt_LinkedIn")],
          [InlineKeyboardButton("X (Twitter) Header", callback_data="plt_X (Twitter)")],
          [InlineKeyboardButton("Facebook Cover", callback_data="plt_Facebook")]]
    await update.message.reply_text("📱 Select your destination social media platform template profile:", reply_markup=InlineKeyboardMarkup(kb))
    return PLATFORM

async def get_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["banner_data"]["platform"] = query.data.split("_")[1]
    
    kb = [[InlineKeyboardButton("Minimalist", callback_data="sty_Minimalist"),
           InlineKeyboardButton("Corporate", callback_data="sty_Corporate")],
          [InlineKeyboardButton("Neon Futuristic", callback_data="sty_Neon"),
           InlineKeyboardButton("Luxury Gold", callback_data="sty_Luxury")]]
    await query.message.reply_text("🎨 Select a visual style template theme:", reply_markup=InlineKeyboardMarkup(kb))
    return STYLE

async def get_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["banner_data"]["style"] = query.data.split("_")[1]
    await query.message.reply_text("🌈 Enter your preferred color scheme palettes description (e.g. Dark mode blue and neon purple glow):")
    return COLORS

async def get_colors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["banner_data"]["colors"] = update.message.text
    await update.message.reply_text("✏ Please describe any extra specific elements, design components, or taglines to include:")
    return DESCRIPTION

async def final_generation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    context.user_data["banner_data"]["desc"] = update.message.text
    await update.message.reply_text("⚡ Awakening generative image matrices... Custom AI design layout compilation running now. Please wait.")
    
    img_url, final_prompt = await banner_generator.generate_banner_url(context.user_data["banner_data"])
    if not img_url:
        await update.message.reply_text("❌ Connection error mapping design array fields via OpenAI matrix vectors.")
        return ConversationHandler.END
        
    processed_file = await image_utils.download_and_crop_banner(img_url, context.user_data["banner_data"]["platform"], uid)
    if processed_file and os.path.exists(processed_file):
        with open(processed_file, "rb") as f:
            await update.message.reply_document(document=f, filename="social_cover.png", caption=f"✨ Render complete! Engineered seamlessly for your platform profile view bounding box dimensions.")
        await database.save_banner_log(uid, final_prompt, img_url)
        image_utils.clean_user_files(uid)
    else:
        await update.message.reply_text("❌ System file storage configuration execution trace lock error.")
    return ConversationHandler.END

async def menu_navigation_routing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    
    if query.data == "nav_specs":
        specs_msg = "📱 *Platform Dimensions Guidelines Matrix:*\n\n- YouTube Art: `2560x1440` (TV Safe Bounds)\n- LinkedIn Cover: `1584x396` (Panels Ratio)\n- X Header: `1500x500` (Dense Landscape)\n- Facebook Layout: `820x312` (Compact Banner)"
        await query.message.reply_text(specs_msg, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
    elif query.data == "nav_logs":
        history = await database.get_user_history(uid)
        if not history:
            await query.message.reply_text("📂 You have not initialized any design generation maps across your logs history index yet.")
        else:
            msg = "📂 *Your Recent Design Prompts Indices:*\n\n" + "\n".join([f"- {item['prompt'][:65]}..." for item in history])
            await query.message.reply_text(msg, reply_markup=keyboards.get_main_menu())
    elif query.data == "nav_help":
        await query.message.reply_text("❓ *Quick Guide:* Tap 'Create Banner', follow the interactive prompt parameters mapping builder loops, and export tailored vector designs.", reply_markup=keyboards.get_main_menu())

