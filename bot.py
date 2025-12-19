import asyncio
import re
import random
import aiohttp
from telethon import TelegramClient, events
from telethon.errors import UsernameInvalidError, ChannelInvalidError, PeerIdInvalidError

# 🔹 TELEGRAM API CREDENTIALS
API_ID = 28746796
API_HASH = '46521fe2050b0cef40030000683bf79d'
SEND_CHAT = '-1003487750858'  # YOUR GROUP ID

# 🔹 LIST OF TELEGRAM CHANNELS/GROUPS TO SCRAPE FROM
chats = [
    '@jdjdhdhdhdhxd', 
    '@MoonScrapperOp', 
    '@cvv_cc_vip',
    '@ramadan_889',
    '@nastylivescrp',
    '@BitchScrV5',
    '@Warnisx_cc_Scrapper',
    -1001878543352, 
    -1002565840193, 
    -1001659933539, 
    -1002662203301, 
    -1002402037749, 
    -1001547217051,
    -1002252838990,
    -1002886988229,
    -1002319403142
]
client = TelegramClient('session', API_ID, API_HASH)

# ✅ BIN LOOKUP API
BIN_API = "https://bins.antipublic.cc/bins/{bin}"

# ✅ COUNTRY FLAGS (Updated to include all recognized countries)
COUNTRY_FLAGS = {
    "AFGHANISTAN": "🇦🇫", "ALBANIA": "🇦🇱", "ALGERIA": "🇩🇿", "ANDORRA": "🇦🇩", "ANGOLA": "🇦🇴",
    "ANTIGUA AND BARBUDA": "🇦🇬", "ARGENTINA": "🇦🇷", "ARMENIA": "🇦🇲", "AUSTRALIA": "🇦🇺", "AUSTRIA": "🇦🇹",
    "AZERBAIJAN": "🇦🇿", "BAHAMAS": "🇧🇸", "BAHRAIN": "🇧🇭", "BANGLADESH": "🇧🇩", "BARBADOS": "🇧🇧",
    "BELARUS": "🇧🇾", "BELGIUM": "🇧🇪", "BELIZE": "🇧🇿", "BENIN": "🇧🇯", "BHUTAN": "🇧🇹",
    "BOLIVIA": "🇧🇴", "BOSNIA AND HERZEGOVINA": "🇧🇦", "BOTSWANA": "🇧🇼", "BRAZIL": "🇧🇷", "BRUNEI": "🇧🇳",
    "BULGARIA": "🇧🇬", "BURKINA FASO": "🇧🇫", "BURUNDI": "🇧🇮", "CABO VERDE": "🇨🇻", "CAMBODIA": "🇰🇭",
    "CAMEROON": "🇨🇲", "CANADA": "🇨🇦", "CENTRAL AFRICAN REPUBLIC": "🇨🇫", "CHAD": "🇹🇩", "CHILE": "🇨🇱",
    "CHINA": "🇨🇳", "COLOMBIA": "🇨🇴", "COMOROS": "🇰🇲", "CONGO, DEMOCRATIC REPUBLIC OF THE": "🇨🇩",
    "CONGO, REPUBLIC OF THE": "🇨🇬", "COSTA RICA": "🇨🇷", "CROATIA": "🇭🇷", "CUBA": "🇨🇺", "CYPRUS": "🇨🇾",
    "CZECHIA": "🇨🇿", "DENMARK": "🇩🇰", "DJIBOUTI": "🇩🇯", "DOMINICA": "🇩🇲", "DOMINICAN REPUBLIC": "🇩🇴",
    "ECUADOR": "🇪🇨", "EGYPT": "🇪🇬", "EL SALVADOR": "🇸🇻", "EQUATORIAL GUINEA": "🇬🇶", "ERITREA": "🇪🇷",
    "ESTONIA": "🇪🇪", "ESWATINI": "🇸🇿", "ETHIOPIA": "🇪🇹", "FIJI": "🇫🇯", "FINLAND": "🇫🇮",
    "FRANCE": "🇫🇷", "GABON": "🇬🇦", "GAMBIA": "🇬🇲", "GEORGIA": "🇬🇪", "GERMANY": "🇩🇪",
    "GHANA": "🇬🇭", "GREECE": "🇬🇷", "GRENADA": "🇬🇩", "GUATEMALA": "🇬🇹", "GUINEA": "🇬🇳",
    "GUINEA-BISSAU": "🇬🇼", "GUYANA": "🇬🇾", "HAITI": "🇭🇹", "HONDURAS": "🇭🇳", "HUNGARY": "🇭🇺",
    "ICELAND": "🇮🇸", "INDIA": "🇮🇳", "INDONESIA": "🇮🇩", "IRAN": "🇮🇷", "IRAQ": "🇮🇶",
    "IRELAND": "🇮🇪", "ISRAEL": "🇮🇱", "ITALY": "🇮🇹", "JAMAICA": "🇯🇲", "JAPAN": "🇯🇵",
    "JORDAN": "🇯🇴", "KAZAKHSTAN": "🇰🇿", "KENYA": "🇰🇪", "KIRIBATI": "🇰🇮", "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF": "🇰🇵",
    "KOREA, REPUBLIC OF": "🇰🇷", "KUWAIT": "🇰🇼", "KYRGYZSTAN": "🇰🇬", "LAOS": "🇱🇦", "LATVIA": "🇱🇻",
    "LEBANON": "🇱🇧", "LESOTHO": "🇱🇸", "LIBERIA": "🇱🇷", "LIBYA": "🇱🇾", "LIECHTENSTEIN": "🇱🇮",
    "LITHUANIA": "🇱🇹", "LUXEMBOURG": "🇱🇺", "MADAGASCAR": "🇲🇬", "MALAWI": "🇲🇼", "MALAYSIA": "🇲🇾",
    "MALDIVES": "🇲🇻", "MALI": "🇲🇱", "MALTA": "🇲🇹", "MARSHALL ISLANDS": "🇲🇭", "MAURITANIA": "🇲🇷",
    "MAURITIUS": "🇲🇺", "MEXICO": "🇲🇽", "MICRONESIA": "🇫🇲", "MOLDOVA": "🇲🇩", "MONACO": "🇲🇨",
    "MONGOLIA": "🇲🇳", "MONTENEGRO": "🇲🇪", "MOROCCO": "🇲🇦", "MOZAMBIQUE": "🇲🇿", "MYANMAR": "🇲🇲",
    "NAMIBIA": "🇳🇦", "NAURU": "🇳🇷", "NEPAL": "🇳🇵", "NETHERLANDS": "🇳🇱", "NEW ZEALAND": "🇳🇿",
    "NICARAGUA": "🇳🇮", "NIGER": "🇳🇪", "NIGERIA": "🇳🇬", "NORTH MACEDONIA": "🇲🇰", "NORWAY": "🇳🇴",
    "OMAN": "🇴🇲", "PAKISTAN": "🇵🇰", "PALAU": "🇵🇼", "PANAMA": "🇵🇦", "PAPUA NEW GUINEA": "🇵🇬",
    "PARAGUAY": "🇵🇾", "PERU": "🇵🇪", "PHILIPPINES": "🇵🇭", "POLAND": "🇵🇱", "PORTUGAL": "🇵🇹",
    "QATAR": "🇶🇦", "ROMANIA": "🇷🇴", "RUSSIA": "🇷🇺", "RWANDA": "🇷🇼", "SAINT KITTS AND NEVIS": "🇰🇳",
    "SAINT LUCIA": "🇱🇨", "SAINT VINCENT AND THE GRENADINES": "🇻🇨", "SAMOA": "🇼🇸", "SAN MARINO": "🇸🇲",
    "SAO TOME AND PRINCIPE": "🇸🇹", "SAUDI ARABIA": "🇸🇦", "SENEGAL": "🇸🇳", "SERBIA": "🇷🇸", "SEYCHELLES": "🇸🇨",
    "SIERRA LEONE": "🇸🇱", "SINGAPORE": "🇸🇬", "SLOVAKIA": "🇸🇰", "SLOVENIA": "🇸🇮", "SOLOMON ISLANDS": "🇸🇧",
    "SOMALIA": "🇸🇴", "SOUTH AFRICA": "🇿🇦", "SOUTH SUDAN": "🇸🇸", "SPAIN": "🇪🇸", "SRI LANKA": "🇱🇰",
    "SUDAN": "🇸🇩", "SURINAME": "🇸🇷", "SWEDEN": "🇸🇪", "SWITZERLAND": "🇨🇭", "SYRIA": "🇸🇾",
    "TAIWAN": "🇹🇼", "TAJIKISTAN": "🇹🇯", "TANZANIA": "🇹🇿", "THAILAND": "🇹🇭", "TIMOR-LESTE": "🇹🇱",
    "TOGO": "🇹🇬", "TONGA": "🇹🇴", "TRINIDAD AND TOBAGO": "🇹🇹", "TUNISIA": "🇹🇳", "TURKEY": "🇹🇷",
    "TURKMENISTAN": "🇹🇲", "TUVALU": "🇹🇻", "UGANDA": "🇺🇬", "UKRAINE": "🇺🇦", "UNITED ARAB EMIRATES": "🇦🇪",
    "UNITED KINGDOM": "🇬🇧", "UNITED STATES": "🇺🇸", "URUGUAY": "🇺🇾", "UZBEKISTAN": "🇺🇿", "VANUATU": "🇻🇺",
    "VENEZUELA": "🇻🇪", "VIETNAM": "🇻🇳", "YEMEN": "🇾🇪", "ZAMBIA": "🇿🇲", "ZIMBABWE": "🇿🇼",
    # Additional recognized entities
    "KOSOVO": "🇽🇰", "PALESTINE": "🇵🇸", "VATICAN CITY": "🇻🇦", "HONG KONG": "🇭🇰", "MACAU": "🇲🇴"
}

# ✅ CACHE FOR SKIPPING DUPLICATES
scraped_ccs = set()

# ✅ EXTRACT CC DETAILS
def getcards(text: str):
    text = text.replace('\n', ' ').replace('\r', '')
    match = re.search(r'(\d{13,16})[| ](\d{1,2})[| ](\d{2,4})[| ](\d{3,4})', text)
    if not match:
        return None
    cc, mes, ano, cvv = match.groups()
    if len(ano) == 2:
        ano = f"20{ano}"
    return cc, mes, ano, cvv

# ✅ GET BIN INFO
async def get_bin_info(cc):
    bin_number = cc[:6]
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with aiohttp.ClientSession() as session:
            url = BIN_API.format(bin=bin_number)
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    country = data.get("country_name", "UNKNOWN").upper()
                    country_flag = COUNTRY_FLAGS.get(country, "🌍")
                    bank_full = data.get("bank", "UNKNOWN").upper()
                    card_type = data.get("type", "UNKNOWN").upper()
                    brand = data.get("brand", "UNKNOWN").upper()

                    if country == "UNKNOWN" or bank_full == "UNKNOWN":
                        return None

                    bank_words = bank_full.split()
                    bank = " ".join(bank_words[:2])

                    issuer_words = bank_full.split()
                    issuer = " ".join(issuer_words[:3])

                    card_info = f"{card_type} - {brand} - BUSINESS"

                    return {
                        "bin": bin_number,
                        "country": country,
                        "country_flag": country_flag,
                        "bank": bank,
                        "issuer": issuer,
                        "card_info": card_info
                    }
    except Exception as e:
        print(f"❌ BIN Lookup Failed: {e}")
    return None

# ✅ SEND MESSAGE TO CHANNEL
async def send_message_to_channel(message):
    BOT_TOKEN = '8598292765:AAHHGmhdg9MrMpOtjQwS7RDm6wU1OMbApbg'
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    params = {
        "chat_id": SEND_CHAT,
        "text": message,
        "parse_mode": "HTML"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                print("✅ Message sent successfully")
            else:
                print(f"❌ Failed to send message: {await response.text()}")

# ✅ VALIDATE CHATS
async def validate_chats(client, chats):
    valid_chats = []
    for chat in chats:
        try:
            entity = await client.get_input_entity(chat)
            valid_chats.append(chat)
            print(f"✅ Valid chat: {chat}")
        except (UsernameInvalidError, ChannelInvalidError, PeerIdInvalidError) as e:
            print(f"❌ Invalid chat: {chat} - {str(e)}")
        except Exception as e:
            print(f"❌ Error validating chat {chat}: {str(e)}")
    return valid_chats

# ✅ TELEGRAM SCRAPING EVENT
@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        text = event.raw_text
        print(f"Received message: {text}")
        card_details = getcards(text)

        if card_details:
            cc, mes, ano, cvv = card_details

            if cc in scraped_ccs:
                print("⏩ Duplicate CC, skipping...")
                return
            scraped_ccs.add(cc)

            bin_info = await get_bin_info(cc)
            if bin_info:
                country = bin_info["country"]
                country_flag = bin_info["country_flag"]
                card_info = bin_info["card_info"]
                bank = bin_info["bank"]
                issuer = bin_info["issuer"]
                bin_number = bin_info["bin"]

                cc_details = f"<code>{cc}|{mes}|{ano}|{cvv}</code>"
                random_digits = f"{random.randint(0, 9999):04d}"
                extra_gen = f"<code>/gen {cc[:8
                                             ]}{random_digits}|{mes}|{ano}|rnd</code>"

                header_link = "https://t.me/HG_SCRAPER"
                cc_link = "https://t.me/HG_SCRAPER"
                bin_link = "https://t.me/HG_SCRAPER"
                time_link = "https://t.me/HG_SCRAPER"

                message = f"""
<b>[<a href="{header_link}">⌬</a>]</b> <b>HG Scrapers</b>  
━━━━━━━━━━━━━  
<b>[<a href="{cc_link}">ϟ</a>]</b> <b>CC :</b> {cc_details}  
<b>[<a href="{cc_link}">ϟ</a>]</b> <b>EXTRA :</b> {extra_gen}  
━━━━━━━━━━━━━  
<b>[<a href="{bin_link}">ᛟ</a>]</b> <b>Bin :</b> <code>{bin_number}</code>  
<b>[<a href="{bin_link}">ᛟ</a>]</b> <b>Info :</b> <code>{card_info}</code>  
<b>[<a href="{bin_link}">ᛟ</a>]</b> <b>Country :</b> <code>{country} - [{country_flag}]</code>  
<b>[<a href="{bin_link}">ᛟ</a>]</b> <b>Issuer :</b> <code>{issuer}</code>  
━━━━━━━━━━━━━  
<b>[<a href="{time_link}">⌯</a>]</b> <b>T/t :</b><code>[{random.uniform(5, 10):.2f}sec]</code> <b>Proxy :</b> <code>[Live ⛅]</code>  
<b>[<a href="{time_link}">⌯</a>]</b> <b>Developer :</b> <code>@CODExHYPER</code>  
<b>[<a href="{time_link}">⌯</a>]</b> <code>Only For Educational Purpose</code>  
━━━━━━━━━━━━━
"""

                await send_message_to_channel(message)
            else:
                print("❌ Failed to retrieve BIN info, skipping...")
        else:
            print("❌ No valid card details found in the message.")
    except Exception as e:
        print(f"❌ Error in event handler: {e}")

# ✅ MAIN FUNCTION
async def main():
    # Validate chats before starting the event handler
    valid_chats = await validate_chats(client, chats)
    
    if not valid_chats:
        print("❌ No valid chats found. Exiting...")
        return
    
    # Update the event handler with valid chats
    client.remove_event_handler(my_event_handler)
    client.on(events.NewMessage(chats=valid_chats))(my_event_handler)
    
    print(f"✅ Listening to {len(valid_chats)} valid chats: {valid_chats}")
    await client.run_until_disconnected()

# ✅ START THE TELEGRAM CLIENT
with client:
    client.loop.run_until_complete(main())