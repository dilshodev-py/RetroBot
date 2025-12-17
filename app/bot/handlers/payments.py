from turtledemo.nim import HUNIT

from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from app.bot.dispatcher import dp


@dp.message(Command('invoice'))
async def invoice(message: Message):
    prices = [
        LabeledPrice(label='Iphone 15 pro', amount=1000*1 * 100),
        LabeledPrice(label='Iphone 14 pro', amount=2000*1 * 100)
    ]
    await message.answer_invoice('Products', "Jami 3 product order qilindi", '1', "UZS",prices= prices, provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065')

@dp.pre_checkout_query()
async def success_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(True)

@dp.message(lambda message: bool(message.successful_payment))
async def confirm_handler(message: Message):
    if message.successful_payment:
        total_amount = message.successful_payment.total_amount//100
        order_id = int(message.successful_payment.invoice_payload)
        # await Order.update(id_=order_id, status=Order.OrderStatusEnum.APPROVED , total_amount = total_amount)
        await message.answer(text=f"To'lo'vingiz uchun raxmat 😊 \n{total_amount}\n{order_id}")

