from flask import Flask, render_template
from flask import Flask, request, redirect
import barcode
import re
from collections import Counter
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

def generate_ean(value):
  images_dir = 'static/images/'
  if len(value) == 6:
    upc_e = barcode.get_barcode_class('upce')
    convert_upc = upc_e(value) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')
  if len(value) == 8:
    ean_8 = barcode.get_barcode_class('ean8')
    convert_ean = ean_8(value) 
    generated_qr = convert_ean.save(f'{images_dir}{value}')
  if len(value) == 12:
    upc_a = barcode.get_barcode_class('upca')
    convert_upc = upc_a(value) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')
  if len(value) == 13: 
    hr = barcode.get_barcode_class('ean13')
    Hr = hr(value)  
    generated_qr = Hr.save(f'{images_dir}{value}')
  if len(value) == 7 or len(value) == 9 or len(value) == 11:
    code39 = barcode.get_barcode_class('code39')
    convert_upc = code39(value, add_checksum=False) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')

def remove_leading_zero(string):
  string = re.sub("^0+", "", string)
  return string

@app.route('/')
def inicio():
  return render_template('form.html')

@app.route('/imagenes')
def mostrar_imagenes():
  with open('Salidapazosnuevo.txt', 'r') as f:
    tickets = {}
    barcodes = {}
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
        tickets[ticket_number] = {'cashier_code': values_line[2], 'number_of_items': values_line[7], 'total_to_pay': values_line[8], 'qr_code': [], 'barcodes': []}
      elif values_line[0] == "L" and values_line[2] == "1":
        tickets[ticket_number]['qr_code'].append(remove_leading_zero(values_line[25]))
        # barcodes[remove_leading_zero(values_line[25])] = int(float(remove_leading_zero(values_line[5])))
        # tickets[ticket_number]['barcodes'].append(barcodes)
        tickets[ticket_number]['barcodes'].append(remove_leading_zero(values_line[25]))
        tickets[ticket_number]['barcodes'].append(str(int(float(remove_leading_zero(values_line[5])))))
  
  # for ticket_number, ticket_data in tickets.items():
  #   print(f'----- {ticket_number} -----')
  #   for i, elem in enumerate(ticket_data["barcodes"]):
  #     if i % 2 == 0:
  #       print(f'{elem} ----------------')
  #     print(elem)
  
  lst = [1, 2, 4, 6, 7, 8, 3, 5]

  for i in range(0, len(lst), 2):
    val_i = lst[i]
    val_i_plus_1 = lst[i+1]
    print(f"val_i: {val_i}, val_i_plus_1: {val_i_plus_1}")

  return render_template('template.html', tickets=tickets)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  # obtenemos el archivo del input "archivo"
  f = request.files['file']
  filename = secure_filename(f.filename)
  location_file = os.path.join(os.getcwd(), 'Salidapazosnuevo.txt')
  f.save(location_file)
    # file = request.files.get('file')
    # if file:
    #     # Procesar el archivo aquí
    #     return 'Archivo cargado exitosamente'
    # else:
    #     return 'No se ha seleccionado ningún archivo'
  # return render_template('form.html')
  return redirect('/imagenes')

if __name__ == '__main__':
  app.run(debug=True)