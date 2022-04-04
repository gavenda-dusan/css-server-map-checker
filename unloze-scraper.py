import asyncio
from pyppeteer import launch
from pyppeteer.page import Page

from lib import discord_send_message

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://stats.unloze.com/hlstats.php?game=css-ze')
    server = 'UNLOZE'

    map_name = await get_unloze_map_name(page)

    if map_name.lower().find('mako_reactor') != -1:
        discord_send_message(f'@everyone current map on {server}: {map_name}')

    await page.goto('https://nide.gg/servers/')
    server = 'NIDE'

    map_name = await get_nide_map_name(page)

    if map_name.lower().find('mako_reactor') != -1:
        discord_send_message(f'@everyone current map on {server}: {map_name}')
        
    await browser.close()

async def get_unloze_map_name(page: Page) -> str:
    return await page.evaluate('document.querySelectorAll("#accordion tr")[2].cells[2].innerText')

async def get_nide_map_name(page: Page) -> str:
    return await page.evaluate('document.querySelectorAll(".ipsDataItem_subList")[0].innerText')

asyncio.get_event_loop().run_until_complete(main())