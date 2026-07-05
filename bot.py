import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import database
import handlers
from config import BOT_TOKEN

def main():
    # Enforce safe asynchronous context boundaries loop to guarantee non-blocking SQLite setup hooks execution
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database.init_db())

    if not BOT_TOKEN:
        print("Fatal error: Missing BOT_TOKEN environmental parameters setting mapping.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    creative_wizard = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.start_creation_flow, pattern="^nav_create$")],
        states={
            handlers.BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_brand)],
            handlers.PLATFORM: [CallbackQueryHandler(handlers.get_platform, pattern="^plt_")],
            handlers.STYLE: [CallbackQueryHandler(handlers.get_style, pattern="^sty_")],
            handlers.COLORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_colors)],
            handlers.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.final_generation)]
        },
        fallbacks=[CommandHandler("start", handlers.start)]
    )

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.menu_navigation_routing, pattern="^nav_"))
    app.add_handler(creative_wizard)

    print("BannerCraft AI Processing Clusters Engaged & Polling live...")
    app.run_polling()

if __name__ == "__main__":
    main()

