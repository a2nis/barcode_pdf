import barcode

def generate_ean(valor):
  if len(valor) == 13: 
    hr = barcode.get_barcode_class('ean13')
    Hr = hr(valor)  #8430469156277
    qr = Hr.save(valor)
  if len(valor) == 8:
    ean_8 = barcode.get_barcode_class('ean8')
    convert_ean = ean_8(valor) # 74200153
    qr_ean8 = convert_ean.save(valor)
  if len(valor) == 12:
    upc_a = barcode.get_barcode_class('upca')
    convert_upc = upc_a(valor) #877012000010
    qr_ean_upc = convert_upc.save(valor)

generate_ean("877012000010")