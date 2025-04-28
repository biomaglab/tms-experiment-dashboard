import locale
from datetime import datetime

# Define a localidade para português do Brasil
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# Obtém o timestamp atual
x = datetime.now().timestamp()

# Converte e formata a data e hora
data_hora = datetime.fromtimestamp(x)
data_formatada = data_hora.strftime("%d %B %Y (%A) às %H:%M:%S %p")
hora_formatada = data_hora.strftime("%H:%M:%S %p")
minutos_formatados = data_hora.strftime("%M:%S %p")

print(data_formatada)
print(hora_formatada)
print(minutos_formatados)
