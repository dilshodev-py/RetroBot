from datetime import date

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.bot.buttons.inline import make_inline_buttons
from app.bot.dispatcher import dp
from db.models import Food, Order, OrderItem
from aiogram.utils.i18n import lazy_gettext as __


@dp.message(F.text == __('🥙 Menu'))
async def menu_handler(message: Message):
    today = date.today()
    foods: [Food] = Food().get()
    btns = [(food.name, f"food_{food.id}") for food in foods]
    size = [1]
    markup = make_inline_buttons(btns , size , repeat=True)
    await message.answer(f"Bugungi sana : {today}" , reply_markup=markup)



@dp.callback_query(F.data.startswith("food_"))
async def food_handler(callback: CallbackQuery):
    await callback.message.delete()
    food_id: int  = int(callback.data.split("_")[1])
    food = Food(id = food_id).get()[0]
    caption = f"""{food.name}\n{food.description}\nsotuvda {food.quantity} ta bor\nNarxi: {food.price}"""
    btns = [("Savatga qo'shish" , f"order_add_{food_id}") , ("🥙 Menyu"  , "menu")]
    markup = make_inline_buttons(btns , [1] , repeat=True)
    await callback.message.answer_photo(photo=food.photo , caption=caption , reply_markup=markup)



@dp.callback_query(F.data.startswith("order_add_"))
async def order_add_handler(callback: CallbackQuery , state: FSMContext):
    food_id = int(callback.data.split("_")[2])
    food = Food(id = food_id).get()[0]
    await state.set_data({"food" : food})
    carts: [Order] = Order(user_id=callback.from_user.id , status='process').get()
    if not carts:
        Order(user_id=callback.from_user.id).save()
        cart: Order = Order(user_id=callback.from_user.id , status='process').get()[0]
    else:
        cart: Order = carts[0]

    count = 1
    btns = [
        ('-' , f'count_{count-1}'),
        (f'🛒({count})' , f"cart_{food_id}") ,
        ('+' , f'count_{count+1}'),
        ("Savatga o'tish -> 🛒" , f'cart_{food_id}'),
        ("🥙 Menyu" , f'menu'),
    ]
    size = [3 , 1,1]
    markup = make_inline_buttons(btns , size)
    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(F.data.startswith('count_'))
async def count_change_handler(callback : CallbackQuery , state: FSMContext):
    count = int(callback.data.split("_")[1])
    data = await state.get_data()
    food = data.get("food")
    food_id = food.id
    if count == 0:
        await callback.answer("1 dan kam bo'lmasin",show_alert=True)
    elif count == food.quantity + 1:
        await callback.answer("Mahsulot soni cheklangan",show_alert=True)
    else:
        btns = [
            ('-', f'count_{count - 1}'),
            (f'🛒({count})', f"cart_{food_id}"),
            ('+', f'count_{count + 1}'),
            ("Savatga qo'shish -> 🛒", f'cart_{food_id}_{count}'),
            ("🥙 Menyu", f'menu'),
        ]
        size = [3, 1, 1]
        markup = make_inline_buttons(btns, size)
        await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(F.data.startswith("cart_"))
async def order_add_handler(callback : CallbackQuery):
    food_id=int(callback.data.split("_")[1])
    count = int(callback.data.split("_")[2])
    cart = Order(user_id=callback.from_user.id , status='process').get()[0]
    OrderItem(order_id=cart.id , count=count , food_id=food_id).save()
    btns = [
        ("Savatga qo'shildi ✅", f'test'),
        ("Savatga o'tish -> 🛒 ", f'cart'),
        ("🥙 Menyu", f'menu'),
    ]
    size = [1]
    markup = make_inline_buttons(btns, size , repeat=True)
    await callback.message.edit_reply_markup(reply_markup=markup)













