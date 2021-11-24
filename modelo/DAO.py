from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Boolean,BLOB,CHAR,Float,ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import relationship

db=SQLAlchemy()

class Usuario(UserMixin,db.Model):
    __tablename__='usuarios'
    idUsuario=Column(Integer,primary_key=True)
    idDireccion = Column(Integer,ForeignKey('direcciones.idDireccion'))
    nombre=Column(String(80),nullable=False)
    telefono=Column(String(10),nullable=False)
    estatus = Column(Boolean, nullable=True)
    tipo = Column(String(20), nullable=False, default='Cliente')
    correo=Column(String(80),unique=True)
    contrasena=Column(String(50),nullable=False)
    direccion = relationship('direcciones',backref='direcciones',lazy='select')

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.estatus

    def is_admin(self):
        if self.tipo == 'Admin':
            return True
        else:
            return False

    def is_cliente(self):
        if self.tipo == 'Cliente':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id (self):
        return self.idUsuario

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.commit

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral (self):
        return self.query.all()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def validar(self,correo,contrasena):
        usuario = None
        usuario = self.query.filter(Usuario.correo ==correo, Usuario.contrasena==contrasena, Usuario.estatus==1).first()
        return usuario;

class direcciones(db.Model):
    __tablename__ = 'direcciones'
    idDireccion = Column(Integer, primary_key=True)
    calle = Column(String(45), nullable=False)
    codigoPostal = Column(String(5), nullable=False)
    descripcion = Column(String(255), nullable=False)
    ciudad = Column(String(45), nullable=False)
    colonia= Column(String(45), nullable=False)
    instruccionEntrega = Column(String(45),nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

class Producto(db.Model):
    __tablename__='productos'
    idProducto = Column(Integer,primary_key=True)
    idFoto = Column(Integer, ForeignKey('fotos.idFoto'))
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(255), nullable=False)
    precioVenta = Column(Float, nullable=False)
    estatus = Column(String(1), nullable=False)
    categoria = Column(String(150), nullable=False)
    fotos = relationship('fotos',backref='direcciones',lazy='select')

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()
    def consultaGeneral(self):
        return self.query.all()

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)


class fotos(db.Model):
    __tablename__='fotos'
    idFoto =Column(Integer,primary_key=True)
    fotografia=Column(BLOB,nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)


class Talla(db.Model):
    __tablename__='tallas'
    idTalla = Column(Integer,primary_key=True)
    nombreTalla = Column(CHAR(5), nullable=False)
    medidas = Column(String(45), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)


    def actualizar(self):
        db.session.merge(self)
        db.session.commit()


class Prenda(db.Model):
    __tablename__='prendas'
    idPrenda = Column(Integer,primary_key=True)
    Productos_idProducto = Column(Integer, ForeignKey('productos.idProducto'))
    Tallas_idTalla = Column(Integer, ForeignKey('tallas.idTalla'))
    unidadesExistencia = Column(Integer, nullable=False)
    color = Column(String(45), nullable=False)
    genero = Column(String(1), nullable=False)
    producto = relationship('Producto', lazy='select')
    talla = relationship('Talla', lazy='select')

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def consultaGeneral(self):
        return self.query.all()

    def insertar(self):
        db.session.add(self)
        db.session.commit()

class Comestible(db.Model):
    __tablename__='comestibles'
    idComestible = Column (Integer, primary_key=True)
    Productos_idProducto = Column (Integer, ForeignKey('productos.idProducto'))
    Sabores_idSabor = Column (Integer, ForeignKey('sabores.idSabor'))
    unidadesExistencia = Column(Integer, nullable=False)
    producto = relationship('Producto', lazy ='select')
    sabor = relationship('Sabores', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

class Sabores(db.Model):
    __tablename__ ='sabores'
    idSabor = Column(Integer, primary_key=True)
    nombreSabor = Column(String(45), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

class Suvenir(db.Model):
    __tablename__ = 'suvenirs'
    idSuvenir = Column (Integer, primary_key=True)
    Productos_idProducto = Column(Integer, ForeignKey('productos.idProducto'))
    unidadesExistencia = Column(Integer, nullable=False)
    producto = relationship('Producto', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()