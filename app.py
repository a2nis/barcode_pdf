import barcode
import re
from collections import Counter

def generate_ean(value):
  if len(value) == 13: 
    hr = barcode.get_barcode_class('ean13')
    Hr = hr(value)  #8430469156277
    qr = Hr.save(value)
  if len(value) == 8:
    ean_8 = barcode.get_barcode_class('ean8')
    convert_ean = ean_8(value) # 74200153
    qr_ean8 = convert_ean.save(value)
  if len(value) == 12:
    upc_a = barcode.get_barcode_class('upca')
    convert_upc = upc_a(value) #877012000010
    qr_ean_upc = convert_upc.save(value)

def remove_leading_zero(string):
  string = re.sub("^0+", "", string)
  return string

with open('Salidapazosnuevo.txt', 'r') as f:
  tickets = {}
  for line in f:
    if not line.strip():
      continue
    values_line = line.split("|")
    if values_line[0] == "C" and values_line[1] == "1":
      ticket_number = values_line[3]
      tickets[ticket_number] = {'cashier_code': values_line[2], 'number_of_items': values_line[7], 'total_to_pay': values_line[8], 'qr_code': []}
    elif values_line[0] == "L" and values_line[2] == "1":
      tickets[ticket_number]['qr_code'].append(remove_leading_zero(values_line[25]))
      
for ticket_number, ticket_data in tickets.items():
  print(ticket_number)
  for value in ticket_data["qr_code"]:
    print(value)
    generate_ean(value)  
  # print(f'Ticket {ticket_number}: QRs = {ticket_data["qr_code"]}' )

# print(Counter(tickets['1226']['qr_code']))

# read_data()