from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from random import choice
import requests
from config_data.config import Config, load_config

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер срабатывает на 'готово'
# Добавим рандомный url
config: Config = load_config()
token = config.tg_bot.api_token
query = ['nice', 'you are awesome', 'very good', 'big thank you']
API_SITE_URL = f'https://api.giphy.com/v1/gifs/search?api_key={token}&q={choice(query)}'

api_updates = requests.get(f'{API_SITE_URL}').json()

urls = []
if api_updates['data']:
    for data in api_updates['data']:
        urls.append(data['images']['original']['url'])


@router.message(F.text.lower() == 'готово')
async def process_ready_answer(message: Message):
    await message.answer_animation(animation=choice(urls))
