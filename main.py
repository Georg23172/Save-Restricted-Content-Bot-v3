# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
import importlib
import os
import sys
import threading

from shared_client import start_client
from pyrogram import idle

# ----------------- Dummy Web Server للحفاظ على Railway حي -----------------
from flask import Flask
web_app = Flask("dummy")

@web_app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    web_app.run(host="0.0.0.0", port=5000)

# تشغيل السيرفر في Thread مستقل
threading.Thread(target=run_flask).start()

# ----------------- تشغيل البوت -----------------
async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def main():
    print("Starting clients ...")
    await load_and_run_plugins()

    # إبقاء البوت يعمل
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(e)
        sys.exit(1)
