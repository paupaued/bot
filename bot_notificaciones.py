import telegram
from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading
from telegram import Bot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Reemplaza esto con tu Token del BotFather
TOKEN = "7524243957:AAHHBjhRJhGXZziEgEt07MAPglExpLRVtIw"

# Reemplaza esto con tu ID de Chat 
CHAT_ID = "6859303261"

# Crear instancia del bot
bot = Bot(token=TOKEN)
bot = telegram.Bot(token=TOKEN)



# Configuración de la API de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(credentials)

# Abre la hoja de cálculo
spreadsheet = gc.open("Planificacion_12_Semanas_estudios")  # Cambia esto por el nombre exacto de tu Google Sheets
worksheet = spreadsheet.sheet1  # Abre la primera hoja de cálculo




try:
    print("📖 Probando conexión con Google Sheets...")
    datos = worksheet.get_all_values()
    if datos:
        for fila in datos:
            print(fila)
    else:
        print("⚠️ La hoja de cálculo está vacía o no tiene acceso.")
except Exception as e:
    print(f"❌ Error al leer Google Sheets: {e}")



# Enviar un mensaje de prueba
def enviar_notificacion():
    print("Intentando enviar notificación...")
    try:
        # Obtener el día actual (0 = Lunes, 6 = Domingo)
        dia_actual = time.localtime().tm_wday
        print(f"Día actual (0=Lunes, 6=Domingo): {dia_actual}")

        # Mapear días de la semana a las columnas
        columnas = {
            0: "B",  # Lunes
            1: "C",  # Martes
            2: "D",  # Miércoles
            3: "E",  # Jueves
            4: "F",  # Viernes
            5: "G",  # Sábado
            6: "H"   # Domingo
        }

        # Leer el contenido de la columna correspondiente
        columna = columnas[dia_actual]
        rango_datos = f"{columna}4:{columna}10"  # Ajustar el rango si es necesario
        datos_dia = worksheet.get_values(rango_datos)

        # Unir los datos en un solo mensaje
        mensaje = "\n".join([fila[0] for fila in datos_dia if fila])
        
        if mensaje:
            # Enviar el mensaje
            bot.send_message(chat_id=CHAT_ID, text=f"📌 Plan de estudio para hoy:\n\n{mensaje}")
            print(f"✅ Mensaje enviado: {mensaje}")
        else:
            print("⚠️ No se encontró mensaje para el día actual en Google Sheets.")
    except Exception as e:
        print(f"❌ Error al enviar el mensaje: {e}")


# Programar el envío diario (Ejemplo: 9:00 AM)
schedule.every().day.at("09:21").do(enviar_notificacion)

# Función para mantener el bot ejecutándose
def ejecutar_scheduler():
    while True:
        print("Revisando tareas programadas...")
        schedule.run_pending()
        time.sleep(60)  # Espera un minuto antes de volver a revisar

# Iniciar el bot en un hilo separado
hilo = threading.Thread(target=ejecutar_scheduler)
hilo.start()

print("✅ Bot de notificaciones en ejecución. Esperando próximos recordatorios...")


