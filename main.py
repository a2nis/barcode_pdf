from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
  return 'Hola, mundo!'

@app.route('/imagenes')
def mostrar_imagenes():
  imagenes = [
    {"nombre": '1234', 
     "qr":'/static/images/1_qr_test.gif',
     "cantidad": 1},
    {"nombre": '4321', 
     "qr":'/static/images/2_qr_test.gif',
     "cantidad": 1},
    {"nombre": '1234', 
     "qr":'/static/images/1_qr_test.gif',
     "cantidad": 1},
    {"nombre": '4321', 
     "qr":'/static/images/2_qr_test.gif',
     "cantidad": 1},
    {"nombre": '1234', 
     "qr":'/static/images/1_qr_test.gif',
     "cantidad": 1},
    {"nombre": '4321', 
     "qr":'/static/images/2_qr_test.gif',
     "cantidad": 5},
    {"nombre": '1234', 
     "qr":'/static/images/1_qr_test.gif',
     "cantidad": 1},
    {"nombre": '4321', 
     "qr":'/static/images/2_qr_test.gif',
     "cantidad": 1},
    {"nombre": '1234', 
     "qr":'/static/images/1_qr_test.gif',
     "cantidad": 1},
    {"nombre": '4321', 
     "qr":'/static/images/2_qr_test.gif',
     "cantidad": 2},
  ]
  return render_template('template.html', imagenes=imagenes)

if __name__ == '__main__':
  app.run(debug=True)