import os
import asyncio
import time
import re
import cloudscraper
import requests
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from vars import Var, API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, api_url, api_token

# Initialize bot
bot = Client(
    "Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

AUTH_USERS = Var.AUTH_USERS

@bot.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(f"**Hello! I'm a downloader bot.**\n\nSend /drm to download videos and PDFs.\nMade by {CREDIT}")

@bot.on_message(filters.command(["restart"]))
async def restart_handler(bot, m):
    if m.from_user.id in AUTH_USERS:
        await m.reply_text("Restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await m.reply_text(f"You are not authorized!\nYour User ID: `{m.from_user.id}`")

@bot.on_message(filters.command(["logs"]))
async def logs_handler(bot, m):
    if m.from_user.id in AUTH_USERS:
        await bot.send_document(m.chat.id, "logs.txt", caption="Bot Logs")
    else:
        await m.reply_text(f"You are not authorized!\nYour User ID: `{m.from_user.id}`")

@bot.on_message(filters.command(["drm"]))
async def txt_handler(bot: Client, m: Message):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(m.chat.id, f"<blockquote>__**Oopss! You are not a Premium member\nPLEASE /upgrade YOUR PLAN\nSend me your user id for authorization\nYour User id**__ - `{m.chat.id}`</blockquote>\n")
        return
    editable = await m.reply_text(f"**__Hii, I am non-drm Downloader Bot__\n<blockquote><i>Send Me Your text file which enclude Name with url...\nE.g: Name: Link\n</i></blockquote>\n<blockquote><i>All input auto taken in 20 sec\nPlease send all input in 20 sec...\n</i></blockquote>**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))  # Extract filename & extension
    path = f"./downloads/{m.chat.id}"
    
    pdf_count = 0
    img_count = 0
    v2_count = 0
    mpd_count = 0
    m3u8_count = 0
    yt_count = 0
    drm_count = 0
    zip_count = 0
    other_count = 0
    
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        
        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif "v2" in url:
                    v2_count += 1
                elif "mpd" in url:
                    mpd_count += 1
                elif "m3u8" in url:
                    m3u8_count += 1
                elif "drm" in url:
                    drm_count += 1
                elif "youtu" in url:
                    yt_count += 1
                elif "zip" in url:
                    zip_count += 1
                else:
                    other_count += 1
        os.remove(x)
    except:
        await m.reply_text("<b>🔹Invalid file input.</b>")
        os.remove(x)
        return
    
    await editable.edit(f"**Total 🔗 links found are {len(links)}\n<blockquote>•PDF : {pdf_count}      •V2 : {v2_count}\n•Img : {img_count}      •YT : {yt_count}\n•zip : {zip_count}       •m3u8 : {m3u8_count}\n•drm : {drm_count}      •Other : {other_count}\n•mpd : {mpd_count}</blockquote>\nSend From where you want to download**")
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'
    
    if int(raw_text) > len(links):
        await editable.edit(f"**🔹Enter number in range of Index (01-{len(links)})**")
        await m.reply_text("**🔹Exiting Task......  **")
        return
        
    await editable.edit(f"**Enter Batch Name or send /d**")
    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text0 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text0 = '/d'
    
    if raw_text0 == '/d':
        b_name = file_name.replace('_', ' ')
    else:
        b_name = raw_text0
    

    await editable.edit("__**Enter resolution or Video Quality (`144`, `240`, `360`, `480`, `720`, `1080`)**__")
    try:
        input2: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text2 = input2.text
        await input2.delete(True)
    except asyncio.TimeoutError:
        raw_text2 = '480'
    quality = f"{raw_text2}p"
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
            ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
    except Exception:
        res = "UN"
        ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"

    await editable.edit(f"**Enter the Credit Name or send /d\n\n<blockquote>Format:\nSend __Admin__ only for caption\nSend __Admin,filename__ for caption and file\nSeparate them with a comma (,)</blockquote>**")
    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text3 = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        raw_text3 = '/d'
        
    if raw_text3 == '/d':
        CR = f"{CREDIT}"
    elif "," in raw_text3:
        CR, PRENAME = raw_text3.split(",")
    else:
        CR = raw_text3

    await editable.edit("**Enter __PW/CP/CW__ Working Token For 𝐌𝐏𝐃 𝐔𝐑𝐋 or send /d**")
    try:
        input4: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text4 = input4.text
        await input4.delete(True)
    except asyncio.TimeoutError:
        raw_text4 = '/d'

    if raw_text4 == '/d':
        cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsIm lkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
        cptoken = "cptoken"
        pwtoken = "pwtoken"
    else:
        cwtoken = raw_text4
        cptoken = raw_text4
        pwtoken = raw_text4
        
    await editable.edit(f"**Send the Video Thumb URL or send /d**")
    try:
        input6: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text6 = input6.text
        await input6.delete(True)
    except asyncio.TimeoutError:
        raw_text6 = '/d'

    if raw_text6.startswith("http://") or raw_text6.startswith("https://"):
        getstatusoutput(f"wget '{raw_text6}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = raw_text6

    await editable.edit("__**⚠️Provide the Channel ID or send /d__\n\n<blockquote><i>🔹 Make me an admin to upload.\n🔸Send /id in your channel to get the Channel ID.\n\nExample: Channel ID = -100XXXXXXXXXXX</i></blockquote>\n**")
    try:
        input7: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text7 = input7.text
        await input7.delete(True)
    except asyncio.TimeoutError:
        raw_text7 = '/d'

    if "/d" in raw_text7:
        channel_id = m.chat.id
    else:
        channel_id = raw_text7    
    await editable.delete()

    try:
        if raw_text == "1":
            batch_message = await bot.send_message(chat_id=channel_id, text=f"<blockquote><b>🎯Target Batch : {b_name}</b></blockquote>")
            if "/d" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
                await bot.pin_chat_message(channel_id, batch_message.id)
                message_id = batch_message.id
                pinning_message_id = message_id + 1
                await bot.delete_messages(channel_id, pinning_message_id)
        else:
            if "/d" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
    except Exception as e:
        await m.reply_text(f"**Fail Reason »**\n<blockquote><i>{e}</i></blockquote>\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}🌟`")

    failed_count = 0
    count = int(raw_text)
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            link0 = "https://" + links[i][1]  # Use original URL for caption

            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            if "," in raw_text3:
                name = f'{PRENAME} {name1[:60]}'
            else:
                name = f'{name1[:60]}'

            # Define ytf for video formats
            ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"

            # Handle Utkarsh URLs
            if "apps-s3-jw-prod.utkarshapp.com" in url and 'enc_plain_mp4' in url:
                url = url.replace(url.split("/")[-1], f"{res}.mp4")
                cmd = f'yt-dlp --add-header "Referer:https://utkarshapp.com/" -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "apps-s3-prod.utkarshapp.com" in url and ".pdf" in url:
                cmd = f'yt-dlp --add-header "Referer:https://utkarshapp.com/" -o "{name}.pdf" "{url}"'
            elif "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "https://cpvod.testbook.com/" in url:
                url = url.replace("https://cpvod.testbook.com/","https://media-cdn.classplusapp.com/drm/")
                url = f"https://drmapijion-botupdatevip.vercel.app/api?url={url}&token={cptoken}"
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])
                cmd = f'yt-dlp {keys_string} -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "classplusapp.com/drm/" in url:
                url = f"https://drmapijion-botupdatevip.vercel.app/api?url={url}&token={cptoken}"
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])
                cmd = f'yt-dlp {keys_string} -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "tencdn.classplusapp" in url:
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{cptoken}'}).json()['url']
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url:
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "edge.api.brightcove.com" in url:
                bcov = f'bcov_auth={cwtoken}'
                url = url.split("bcov_auth")[0]+bcov
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "childId" in url and "parentId" in url:
                url = f"https://anonymousrajputplayer-9ab2f2730a02.herokuapp.com/pw?url={url}&token={pwtoken}"
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={pwtoken}"
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'
            elif ".pdf*" in url:
                url = f"https://dragoapi.vercel.app/pdf/{url}"
                cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]
                cmd = None  # Will be handled by helper.download_and_decrypt_video
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" -o "{name}.mp4" "{url}"'

            try:
                cc = f'[🎥]Vid Id : {str(count).zfill(3)}\n**Video Title :** `{name1} [{res}p] .mkv`\n<blockquote><b>Batch Name :</b> {b_name}\nLink : <a href="{link0}">Click Here</a></blockquote>\n\n**Extracted by➤**{CR}\n'
                cc1 = f'[📕]Pdf Id : {str(count).zfill(3)}\n**File Title :** `{name1} .pdf`\n<blockquote><b>Batch Name :</b> {b_name}\nLink : <a href="{link0}">Click Here</a></blockquote>\n\n**Extracted by➤**{CR}\n'
                cczip = f'[📁]Zip Id : {str(count).zfill(3)}\n**Zip Title :** `{name1} .zip`\n<blockquote><b>Batch Name :</b> {b_name}\nLink : <a href="{link0}">Click Here</a></blockquote>\n\n**Extracted by➤**{CR}\n'
                ccimg = f'[🖼️]Img Id : {str(count).zfill(3)}\n**Img Title :** `{name1} .jpg`\n<blockquote><b>Batch Name :</b> {b_name}\nLink : <a href="{link0}">Click Here</a></blockquote>\n\n**Extracted by➤**{CR}\n'
                ccm = f'[🎵]Audio Id : {str(count).zfill(3)}\n**Audio Title :** `{name1} .mp3`\n<blockquote><b>Batch Name :</b> {b_name}\nLink : <a href="{link0}">Click Here</a></blockquote>\n\n**Extracted by➤**{CR}\n'
                cchtml = f'[🌐]Html Id : {str(count).zfill(3)}\n**Html Title :** `{name1} .html`\n<blockquote><b>Batch Name :</b> {b_name}\nLink : <a href="{link0}">Click Here</a></blockquote>\n\n**Extracted by➤**{CR}\n'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=channel_id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif ".pdf" in url:
                    if "cwmediabkt99" in url or "apps-s3-prod.utkarshapp.com" in url:
                        max_retries = 15
                        retry_delay = 4
                        success = False
                        failure_msgs = []
                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)
                                if response.status_code == 200:
                                    with open(f'{name}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)
                                    copy = await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                                    count += 1
                                    os.remove(f'{name}.pdf')
                                    success = True
                                    break
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)
                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue 
                        for msg in failure_msgs:
                            await msg.delete()
                        if not success:
                            await m.reply_text(f"Failed to download PDF after {max_retries} attempts.\n⚠️**Downloading Failed**⚠️\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}", disable_web_page_preview=True)
                            count += 1
                            failed_count += 1
                            continue
                    else:
                        try:
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            status, output = getstatusoutput(download_cmd)
                            if status == 0 and os.path.exists(f'{name}.pdf'):
                                copy = await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                                count += 1
                                os.remove(f'{name}.pdf')
                            else:
                                await m.reply_text(f"Failed to download PDF:\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}\n**Error** =>> {output}", disable_web_page_preview=True)
                                count += 1
                                failed_count += 1
                                continue
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue    

                elif ".ws" in url and url.endswith(".ws"):
                    try:
                        await helper.pdf_download(f"{api_url}utkash-ws?url={url}&authorization={api_token}", f"{name}.html")
                        time.sleep(1)
                        await bot.send_document(chat_id=channel_id, document=f"{name}.html", caption=cchtml)
                        os.remove(f'{name}.html')
                        count += 1
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        status, output = getstatusoutput(download_cmd)
                        if status == 0 and os.path.exists(f'{name}.{ext}'):
                            copy = await bot.send_photo(chat_id=channel_id, photo=f'{name}.{ext}', caption=ccimg)
                            count += 1
                            os.remove(f'{name}.{ext}')
                        else:
                            await m.reply_text(f"Failed to download image:\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}\n**Error** =>> {output}", disable_web_page_preview=True)
                            count += 1
                            failed_count += 1
                            continue
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        status, output = getstatusoutput(download_cmd)
                        if status == 0 and os.path.exists(f'{name}.{ext}'):
                            copy = await bot.send_document(chat_id=channel_id, document=f'{name}.{ext}', caption=ccm)
                            count += 1
                            os.remove(f'{name}.{ext}')
                        else:
                            await m.reply_text(f"Failed to download audio:\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}\n**Error** =>> {output}", disable_web_page_preview=True)
                            count += 1
                            failed_count += 1
                            continue
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif 'encrypted.m' in url:    
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    res_file = await helper.download_and_decrypt_video(url, cmd, name, appxkey)  
                    filename = res_file  
                    await prog.delete(True)  
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    count += 1  
                    await asyncio.sleep(1)  
                    continue  

                elif 'drmcdni' in url or 'drm/wv' in url:
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                    count += 1
                    await asyncio.sleep(1)
                    continue

                else:
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                    status, output = getstatusoutput(download_cmd)
                    filename = f"{name}.mp4"
                    if status == 0 and os.path.exists(filename):
                        await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id)
                        count += 1
                        os.remove(filename)
                    else:
                        await m.reply_text(f"Failed to download video:\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}\n**Error** =>> {output}", disable_web_page_preview=True)
                        count += 1
                        failed_count += 1
                    await prog.delete(True)
                    await asyncio.sleep(1)
                
            except Exception as e:
                await bot.send_message(channel_id, f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}\n\n<blockquote><i><b>Failed Reason: {str(e)}</b></i></blockquote>', disable_web_page_preview=True)
                count += 1
                failed_count += 1
                continue

    except Exception as e:
        await m.reply_text(f"Error: {str(e)}")
        time.sleep(2)

    success_count = len(links) - failed_count
    video_count = v2_count + mpd_count + m3u8_count + yt_count + drm_count + zip_count + other_count
    if raw_text7 == "/d":
        await bot.send_message(channel_id, f"<b>-┈━═.•°✅ Completed ✅°•.═━┈-</b>\n<blockquote><b>🎯Batch Name : {b_name}</b></blockquote>\n<blockquote>🔗 Total URLs: {len(links)} \n┃   ┠🔴 Total Failed URLs: {failed_count}\n┃   ┠🟢 Total Successful URLs: {success_count}\n┃   ┃   ┠🎥 Total Video URLs: {video_count}\n┃   ┃   ┠📄 Total PDF URLs: {pdf_count}\n┃   ┃   ┠📸 Total IMAGE URLs: {img_count}</blockquote>\n")
    else:
        await bot.send_message(channel_id, f"<b>-┈━═.•°✅ Completed ✅°•.═━┈-</b>\n<blockquote><b>🎯Batch Name : {b_name}</b></blockquote>\n<blockquote>🔗 Total URLs: {len(links)} \n┃   ┠🔴 Total Failed URLs: {failed_count}\n┃   ┠🟢 Total Successful URLs: {success_count}\n┃   ┃   ┠🎥 Total Video URLs: {video_count}\n┃   ┃   ┠📄 Total PDF URLs: {pdf_count}\n┃   ┃   ┠📸 Total IMAGE URLs: {img_count}</blockquote>\n")
        await bot.send_message(m.chat.id, f"<blockquote><b>✅ Your Task is completed, please check your Set Channel📱</b></blockquote>")

bot.run()
