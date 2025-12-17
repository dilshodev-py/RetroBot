from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.bot.buttons.reply import make_reply_buttons
from app.bot.dispatcher import dp
from app.bot.utils import user_exists_or_create
from aiogram.utils.i18n import gettext as _, I18n


class MenuStates(StatesGroup):
    menu = State()
@dp.message(CommandStart())
async def command_start_handler(message: Message , state : FSMContext) -> None:
    user_exists_or_create(message.from_user)
    btns = [_("🥙 Menu") , _("Cart 🛒"), _("Today orders"), 'Uzbek' , "English" , "Russian"]
    size = [2 , 1 , 3]
    await state.set_state(MenuStates.menu)
    markup = make_reply_buttons(btns, size)
    await message.answer(_("Hello"), reply_markup=markup)


@dp.message(MenuStates.menu , F.text.in_({"Uzbek" ,"English" , "Russian" }) )
async def change_language(message: Message , state: FSMContext,i18n:I18n) -> None:
    map_ = {
        "Uzbek": "uz",
        "English": "en",
        "Russian": "ru",
    }
    lang_code = map_.get(message.text)
    i18n.current_locale = lang_code
    await state.set_data({"locale" : lang_code})
    btns = [_("🥙 Menu"), _("Cart 🛒"), _("Today orders"), 'Uzbek', "English", "Russian"]
    size = [2, 1, 3]
    markup = make_reply_buttons(btns, size)
    await message.answer(_("Hello"), reply_markup=markup)








