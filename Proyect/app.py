from flask import Flask, request, render_template, redirect, json
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
db = SQLAlchemy(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'puesto28c@gmail.com'
app.config['MAIL_PASSWORD'] = 'iosg ivbt rbuy lrpu'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Resto del código...

# Diccionario para almacenar la cantidad y tipo de empaque de cada fruta
frutas_disponibles = {
    'Banana': 'Cajon',
    'Banana Bolivia': 'Cajon',
    'Banana Paraguaya': 'Cajon',
    'Banana Ecuador': 'Cajon',
    'Banana Ecuador media': 'Cajon',
    'Manzana': 'Cajon',
    'Manzana Caja': 'Cajon',
    'Manzana Jaula': 'Cajon',
    'Manzana Media': 'Cajon',
    'Naranja': 'Cajon',
    'Naranja jugo': 'Cajon',
    'Naranja Ombligo': 'Cajon',
    'Mandarina': 'Cajon',
    'Mandarina Danci': 'Cajon',
    'Mandarina Criolla': 'Cajon',
    'Pera': 'Cajon',
    'Durazno': 'Cajon',
    'Pelón': 'Cajon',
    'Ciruela': 'Cajon',
    'Uva': 'Cajon',
    'Melón': 'Cajon',
    'Sandia': 'Cajon',
    'Lechuga': 'Cajon',
    'Lechuga Mantecosa': 'Cajon',
    'Lechuga Repollada': 'Cajon',
    'Espinaca': 'Unidad',
    'Acelga': 'Unidad',
    'Apio': 'Unidad',
    'Coliflor': 'Unidad',
    'Brócoli': 'Unidad',
    'Remolacha': 'Unidad',
    'Perejil': 'Unidad',
    'Ajo': 'Unidad',
    'Ajo Chico': 'Unidad',
    'Ajo Mediano': 'Unidad',
    'Ajo Grande': 'Unidad',
    'Tomate': 'Cajon',
    'Tomate Perita': 'Cajon',
    'Tomate Redondo': 'Cajon',
    'Tomate Cherry': 'Cajon',
    'Puerro': 'Unidad',
    'Achicoria': 'Unidad',
    'Rucula': 'Unidad',
    'Papa': 'Bolsa',
    'Papa Blanca': 'Bolsa',
    'Papa Negra': 'Bolsa',
    'Zanahoria Chica': 'Bolsa',
    'Zanahoria Grande': 'Bolsa',
    'Zapallo': 'Bolsa',
    'Calabaza': 'Bolsa',
    'Pimiento rojo': 'Cajon',
    'Pimiento verde': 'Cajon',
    'Berenjena': 'Bolsa o Cajon',
    'Pepino': 'Bolsa',
    'Choclo': 'Bolsa o Cajon'
}


# Ordenar el diccionario alfabéticamente por las claves (frutas)
frutas_disponibles = dict(sorted(frutas_disponibles.items()))

def guardar_pedido(nombre, fruta, cantidad):
    nuevo_pedido = f'Nombre: {nombre}, Fruta: {fruta}, Cantidad: {cantidad}\n'
    with open('pedidos.txt', 'a') as archivo:
        archivo.write(nuevo_pedido)


# Función para verificar disponibilidad de frutas
def verificar_disponibilidad(fruta, cantidad):
    if fruta in frutas_disponibles and cantidad <= frutas_disponibles[fruta]:
        return True
    else:
        return False
    
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    fruta = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

# Mover la creación de la base de datos aquí
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', frutas_disponibles=frutas_disponibles)

# Este código debe ejecutarse solo una vez para crear el archivo
with open('pedidos.txt', 'w') as archivo:
    archivo.write('')

def enviar_correo(nombre, frutas):
    frutas_texto = "\n".join(frutas)  # Convertir la lista de frutas a texto

    msg = Message('Asunto del Correo', sender='frandalpro9@gmail.com', recipients=['puesto28c@gmail.com'])
    msg.body = f"Nuevo pedido recibido:\n\nNombre: {nombre}\nFrutas/Verduras:\n{frutas_texto}"
    mail.send(msg)
    return "Correo enviado correctamente"


@app.route('/submit', methods=['POST'])
def submit():
    print("Submit function called")
    nombre = request.form['nombre']
    frutas = json.loads(request.form.get('frutas'))
    print(f"Nombre: {nombre}, Frutas: {frutas}")

    for fruta in frutas:
        cantidad = int(request.form.get(f'cantidad_{fruta}', 1))
        nuevo_pedido = Pedido(nombre=nombre, fruta=fruta, cantidad=cantidad)
        db.session.add(nuevo_pedido)
        db.session.commit()
        print(f'Pedido almacenado en la base de datos: Nombre: {nombre}, Fruta: {fruta}, Cantidad: {cantidad}')

    enviar_correo(nombre, frutas)  # Enviar el correo al final del proceso

    return f'Pedido recibido. Nombre: {nombre}'


if __name__ == '__main__':
    app.run(debug=True)