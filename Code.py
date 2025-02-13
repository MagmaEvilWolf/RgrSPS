from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
import plotly.express as px
import io
import os
import asyncio
import plotly.io as pio


# Функция для обработки CSV файла и генерации графиков
def generate_graphs_from_csv(file):
    df = pd.read_csv(file)
    df['Дата'] = pd.to_datetime(df['Дата'])
    df.set_index('Дата', inplace=True)

    # Генерация графиков
    figures = []
    total_sales_fig = px.bar(
        df.resample('M').sum().reset_index(),
        x='Дата',
        y='Сумма',
        title='Общие продажи по месяцам',
        template='plotly_dark'
    )

    sales_by_category_fig = px.pie(
        df,
        names='Категория',
        values='Сумма',
        title='Продажи по категориям',
        template='plotly_dark'
    )

    quantity_sold_fig = px.line(
        df.resample('D').sum().reset_index(),
        x='Дата',
        y='Количество',
        title='Количество проданных товаров по датам',
        template='plotly_dark'
    )

    monthly_sales_fig = px.area(
        df.resample('M').sum().reset_index(),
        x='Дата',
        y='Сумма',
        title='Продажи по месяцам',
        template='plotly_dark'
    )

    top_products_fig = px.bar(
        df.groupby('Товар')['Количество'].sum().nlargest(5).reset_index(),
        x='Количество',
        y='Товар',
        orientation='h',
        title='Топ-5 товаров по количеству проданных единиц',
        template='plotly_dark'
    )


    figures.append(total_sales_fig)

    figures.append(sales_by_category_fig)

    figures.append(quantity_sold_fig)

    figures.append(monthly_sales_fig)

    figures.append(top_products_fig)

    print(f"Generated {len(figures)} figures.") # Отладочное сообщение

 # Сохранение графиков в HTML
    html_files = []
    for i, fig in enumerate(figures):
        try:
            # Генерация HTML файла
            html_bytes = pio.to_html(fig, full_html=False) # Генерация HTML
            html_files.append(io.BytesIO(html_bytes.encode('utf8')))
            print(f'HTML файл graph_{i + 1}.html успешно сгенерирован.')
        except Exception as e:
            print(f'Ошибка при обработке фигуры {i}: {e}')
    return html_files
# Обработчик команды /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправьте мне CSV файл с данными о продажах.')
# Обработчик получения файла
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
 # Получаем файл
    file = await update.message.document.get_file()
# Загрузка файла
    await file.download_to_drive('data.csv')
 # Генерация графиков
    html_files = generate_graphs_from_csv('data.csv')
 # Отправка графиков пользователю
    for i, html in enumerate(html_files):
        html.seek(0)
        print(f"Sending HTML file {i + 1}...") # Отладочное сообщение
        try:
            await update.message.reply_document(document=InputFile(html, filename=f'graph_{i + 1}.html'))
            print(f"HTML file {i + 1} sent successfully.")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to send HTML file {i + 1}: {e}")
def main():
    TOKEN = '7279406794:AAHEuoNDMpkOC6cKRwP2emufano1Df5X1eM'

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.MimeType("text/csv"), handle_document))

    app.run_polling()

if __name__ == '__main__':
    main()
