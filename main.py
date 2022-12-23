from flask import Flask, render_template
import barcode
import re
from collections import Counter

app = Flask(__name__)

def generate_ean(value):
  images_dir = 'static/images/'
  if len(value) == 13: 
    hr = barcode.get_barcode_class('ean13')
    Hr = hr(value)  
    generated_qr = Hr.save(f'{images_dir}{value}')
  if len(value) == 8:
    ean_8 = barcode.get_barcode_class('ean8')
    convert_ean = ean_8(value) 
    generated_qr = convert_ean.save(f'{images_dir}{value}')
  if len(value) == 12:
    upc_a = barcode.get_barcode_class('upca')
    convert_upc = upc_a(value) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')
  if len(value) == 6:
    upc_e = barcode.get_barcode_class('upce')
    convert_upc = upc_e(value) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')
  if len(value) == 9:
    code39 = barcode.get_barcode_class('code39')
    convert_upc = code39(value, add_checksum=False) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')

def remove_leading_zero(string):
  string = re.sub("^0+", "", string)
  return string

@app.route('/')
def inicio():
  return 'Hola, mundo!'

@app.route('/imagenes')
def mostrar_imagenes():
  with open('Salidapazosnuevo.txt', 'r') as f:
    tickets = {}
    separator = {
      True : '#',
      False : '|'
    }
    for line in f:
      if not line.strip():
        continue
      if "#" in line:
        numeral_symbol = True
      if "|" in line:
        numeral_symbol = False
      values_line = line.split(separator[numeral_symbol])
      if values_line[0] == "C" and values_line[1] == "1":
        ticket_number = values_line[3]
        tickets[ticket_number] = {'cashier_code': values_line[2], 'number_of_items': values_line[7], 'total_to_pay': values_line[8], 'qr_code': []}
      elif values_line[0] == "L" and values_line[2] == "1":
        tickets[ticket_number]['qr_code'].append(remove_leading_zero(values_line[25]))
  
  for ticket_number, ticket_data in tickets.items():
    for value in ticket_data["qr_code"]:
      generate_ean(value)

  return render_template('template.html', tickets=tickets)

if __name__ == '__main__':
  app.run(debug=True)