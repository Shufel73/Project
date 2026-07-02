import mysql.connector
import telebot

TOKEN = '???????????????'
CHAT_ID = '??????????????'
bot = telebot.TeleBot(TOKEN)
from netmiko import ConnectHandler
def send_telegram_alert(device_name, error_msg):
    text = f"🚨 *NETWORK ALERT* 🚨\n\nDevice: {device_name}\nStatus: DOWN\nError: {error_msg}"
    bot.send_message(CHAT_ID, text,)

devices = [
    {
        'device_name': 'Router-BR-1',
        'device_type': 'cisco_ios',
        'host': '2.2.2.2',
        'username': 'Shufel',
        'password': '1234',
        'global_delay_factor': 2
    },
    {
         'device_name': 'Switch-BR-2',
         'device_type': 'cisco_ios',
         'host': '3.3.3.3',
         'username': 'Shufel',
         'password': '1234',
         'global_delay_factor': 2
    },
    {
        'device_name': 'Router-HQ',
        'device_type': 'cisco_ios',
        'host': '1.1.1.1',
        'username': 'Shufel',
        'password': '1234',
        'global_delay_factor': 2
    },
    {
        'device_name': 'SW-BR-1',
        'device_type': 'cisco_ios',
        'host': '10.10.10.125',
        'username': 'Shufel',
        'password': '1234',
        'global_delay_factor': 2
    },
    {
        'device_name': 'SW-BR-2',
        'device_type': 'cisco_ios',
        'host': '10.10.10.189',
        'username': 'Shufel',
        'password': '1234',
        'global_delay_factor': 2
    },
    {
        'device_name': 'SW-HQ',
        'device_type': 'cisco_ios',
        'host': '10.10.10.61',
        'username': 'Shufel',
        'password': '1234',
        'global_delay_factor': 2
    },
]

print("Starting network scan...")

try:
    
    db_connection = mysql.connector.connect(
        host="localhost",
        user="shufel_db",
        password="123456",
        database="NetworkDB"
    )
    cursor = db_connection.cursor()
    sql = "INSERT INTO NetworkLogs (device_name, status, message) VALUES (%s, %s, %s)"

    
    for device in devices:
        print(f"\nChecking {device['device_name']} ({device['host']})...")
        
        try:
            clean_device = device.copy()
            del clean_device['device_name']
            
            net_connect = ConnectHandler(**clean_device)
            
            output = net_connect.send_command('show version | include uptime')
            
            message = f"SSH successful. {output.strip()}"
            values = (device['device_name'], 'UP', message)
            
            
            cursor.execute(sql, values) 
           
            
            db_connection.commit()
            
            print(f"[+] SUCCESS: Logged {device['device_name']} as UP in database.")
            net_connect.disconnect()

        except Exception as e:
            error_msg = str(e)[:200]
            values = (device['device_name'], 'DOWN', f"SSH Failed: {error_msg}")
            
            
            cursor.execute(sql, values)
            db_connection.commit()
            
            
            print(f"[-] FAILED: Logged {device['device_name']} as DOWN. Sending alert...")
            send_telegram_alert(device['device_name'], error_msg)

except mysql.connector.Error as err:
    print(f"Database error: {err}")

finally:
    
    if 'db_connection' in locals() and db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("\nNetwork scan complete. Database connection closed.")