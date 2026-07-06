# Funciones auxiliares para seguridad, cifrado y manejo de imágenes en Cloudinary.
import bcrypt
import os
from cryptography.fernet import Fernet
from typing import Union
import base64
import cloudinary
import cloudinary.uploader
from werkzeug.datastructures import FileStorage

def hash_password(pwd: str) -> str:
    # Genera un hash seguro para guardar contraseñas sin almacenar el texto plano.
    bytes_pwd = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes_pwd, salt)
    return hashed_pwd.decode('utf-8')

def verify_password(hashed_pwd: str, pwd: str) -> bool:
    # Compara una contraseña recibida con el hash almacenado.
    bytes_hashed_pwd = hashed_pwd.encode('utf-8')
    bytes_pwd = pwd.encode('utf-8')
    return bcrypt.checkpw(bytes_pwd, bytes_hashed_pwd)

class CryptoHelper:
    # Encapsula el cifrado Fernet para proteger valores sensibles como IDs.
    def __init__(self):
        self._key = os.getenv('FERNET_SECRET_KEY')
        self.validate_key()  # Se ejecuta después de asignar la llave
        self.fernet = Fernet(self._key)

    def encrypt(self, value: Union[str, int, float, bool]) -> str:
        string_value = str(value)
        bytes_value = string_value.encode('utf-8')
        encrypted_value = self.fernet.encrypt(bytes_value)
        return encrypted_value.decode('utf-8')
    
    def decrypt(self, value: str) -> int:
        # Forzamos el retorno a entero (int) ya que desencriptarás IDs de usuarios/pacientes
        bytes_value = value.encode('utf-8')
        decrypted_value = self.fernet.decrypt(bytes_value)
        return int(decrypted_value.decode('utf-8'))
    
    def validate_key(self):
        if not self._key:
            raise ValueError('FERNET_SECRET_KEY is not set')
        
        try:
            bytes_key = base64.urlsafe_b64decode(self._key)
            if len(bytes_key) != 32:
                raise ValueError('Invalid key length')
        except ValueError as e:
            raise ValueError(f'Fernet Key Error: {e}')
        
class CloudinaryHelper:
    # Encapsula la configuración y operaciones de imágenes contra Cloudinary.
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            secure=True
        )

    def upload_image(
            self,
            image: FileStorage,
            folder: str = 'doctors'  # Adaptado a tu dominio médico
        ) -> tuple[str, str] | None:
        try:
            response = cloudinary.uploader.upload(
                image,
                folder=folder
            )
            secure_url = response.get('secure_url')
            public_id = response.get('public_id')
            return secure_url, public_id
        except Exception:
            return None
        
    def get_secure_url(self, public_id: str) -> str | None:
        try:
            secure_url = cloudinary.utils.cloudinary_url(
                public_id,
                secure=True
            )
            return secure_url[0]
        except Exception:
            return None
        
    def delete_image(self, public_id: str) -> bool:
        try:
            cloudinary.uploader.destroy(public_id)
            return True
        except Exception:
            return False
        
    def validate_image(self, image: FileStorage) -> bool:
        if not image or image.filename == '':
            raise ValueError('La imagen es obligatoria')
        
        if not image.content_type.startswith('image/'):
            raise ValueError('El archivo proporcionado no es una imagen válida')
            
        return True

cloudinary_helper = CloudinaryHelper()