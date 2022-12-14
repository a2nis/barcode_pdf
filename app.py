import barcode

hr = barcode.get_barcode_class('ean13')
Hr = hr('8430469156277')
qr = Hr.save('ean13')

ean_8 = barcode.get_barcode_class('ean8')
convert_ean = ean_8('74200153')
qr_ean8 = convert_ean.save('ean8')

upc_a = barcode.get_barcode_class('upca')
convert_upc = upc_a('877012000010')
qr_ean_upc = convert_upc.save('upc_a')