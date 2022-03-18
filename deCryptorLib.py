import os
import datetime
import uuid
import base64
# Fernet importing
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class __info__:
	name = "deCryptor"
	version = "0.6-fix"
	versionint = 0.6
	authors = [
		"Роман Слабицкий",
		"Никита Додзин",
		"Марк Метелев",
		"Коломыйцев Алексей"
	]

class __config__:
	work_speed_mod = True

class __func__:
	def encoding(data: bytes, key: bytes) -> bytes:
		"""Принимает данные и ключ, отдаёт зашифрованную байт-строку"""
		return Fernet(key).encrypt(data)

	def decoding(data: bytes, key: bytes) -> bytes:
		"""Принимает данные и ключ, отдаёт расшифрованую байт-строку"""
		return Fernet(key).decrypt(data)

	def encoding_fernet(fernet: Fernet, data: bytes) -> bytes:
		"""Принимает класс Farnet с внедрёным ключём и данные, отдаёт зашифрованную байт-строку"""
		return fernet.encrypt(data)

	def decoding_fernet(fernet: Fernet, data: bytes) -> bytes:
		"""Принимает класс Farnet с внедрёным ключём и данные, отдаёт расшифрованую байт-строку"""
		return fernet.decrypt(data)

	def files_in_folder(folderpath: str) -> list:
		"""Принимает путь к папке и ищит файлы даже в подпапках этой папке, так же можно ввести просто путь файлу"""
		files = []
		folder_abspath = os.path.abspath(folderpath)
		if os.path.isdir(folder_abspath):
			for i in os.listdir(folder_abspath):
				path = folder_abspath + os.sep + i
				if os.path.isdir(path):
					for _i in __func__.files_in_folder(path):
						files.append(_i)
				elif os.path.isfile(path):
					files.append(path)
		elif os.path.isfile(folder_abspath):
			files.append(folder_abspath)
		return files

	def create_key(key_path: str=None, path: str=None) -> str:
		"""Создаёт ключ-файл и отдаёт полный путь к нету"""
		if path != None:
			key_path = os.path.abspath(
				os.path.split(path)[0]
				+ os.sep
				+ os.path.basename(
					key_path
					if (key_path != None)
					else (str(uuid.uuid4()).replace("-", "") + ".key")
				)
			)
		else:
			key_path = os.path.abspath(
				key_path
				if (key_path != None)
				else (str(uuid.uuid4()).replace("-", "") + ".key")
			)
		with open(key_path, "wb") as file:
			file.write(Fernet.generate_key())
		return key_path

	def create_key_from_password(password: str) -> tuple[bytes, bytes]:
		return __func__.password_to_token(
			password,
			algorithm=hashes.SHA256(),
			length=32,
			salt=base64.b64encode(password.encode()),
			iterations=390000
		)
	
	def password_to_token(password: str, *, algorithm, length: int, salt: bytes, iterations: int) -> tuple[bytes, bytes]:
		"""Создаёт ключ из строки, который будет являться паролем от данных"""
		salt = (os.urandom(16)) if (salt is None) else (salt)
		key = base64.urlsafe_b64encode(PBKDF2HMAC(
			algorithm=algorithm,
			length=length,
			salt=salt,
			iterations=iterations
		).derive(password.encode()))
		return base64.b64encode(salt), key

	def load_key(key_path: str) -> bytes:
		"""Принимает путь к ключ-файлу, и отдаёт байтовую строку ключа"""
		with open(key_path, "rb") as file:
			return file.read()

class deCryptor:
	def __init__(self, *, speed_mode=False) -> None:
		self.speed_mode = speed_mode if (__config__.work_speed_mod) else False

	def test_key(self, key: bytes) -> bool:
		"""Вернёт булевое значение, если `True`, то значит ключ рабочий, если `False` - то ключ сломан или не являеться ключом"""
		try:
			fernet = Fernet(key)
			return True
		except:
			return False

	def encode_file(self, path: str, key_path: str = None) -> dict:
		"""Зашифровывает файл(ы) и отдаёт словарь с информацией"""
		start_time_init = datetime.datetime.now()
		# Нормализация путей
		path = os.path.abspath(path)
		if key_path != None:
			key_path = os.path.abspath(key_path)

		# Проверка существования
		if os.path.exists(path):
			files_list = __func__.files_in_folder(path)
		else:
			return {"type": "error", "data": "folder_or_file_does_not_exist"}

		# Проверка наличия файлов
		if len(files_list) == 0:
			return {"type": "error", "data": "no_files_found"}

		# Создание ключа
		if key_path != None:
			if not (os.path.exists(key_path)):
				try:
					key_path = __func__.create_key(key_path, path)
				except:
					return {"type": "error", "data": "failed_to_create_key_file"}
		else:
			try:
				key_path = __func__.create_key(key_path, path)
			except:
				return {"type": "error", "data": "failed_to_create_key_file"}

		# Загрузка ключа
		try:
			key = __func__.load_key(key_path)
		except:
			return {"type": "error", "data": "failed_to_load_key_file"}

		# Тестирование ключа
		if not(self.test_key(key)):
			return {"type": "error", "data": "key_file_is_not_working"}

		# Создание переменых для работы
		files_error = []
		error_block = 0
		file_data = None
		if self.speed_mode:
			try:
				farnet = Fernet(key)
				func_encode = __func__.encoding_fernet
			except:
				return {"type": "error", "data": "failed_to_use_speed_mode"}
		else:
			func_encode = __func__.encoding

		end_time_init = datetime.datetime.now()

		# Работа
		start_cryptor_time = datetime.datetime.now()

		for i in files_list:
			# Чтение
			try:
				with open(i, "rb") as file:
					file_data = file.read()
			except:
				error_block += 1

			# Зашифровка
			try:
				if error_block == 0:
					if self.speed_mode:
						file_data = func_encode(farnet, file_data)
					else:
						file_data = func_encode(file_data, key)
			except:
				error_block += 1

			# Запись
			try:
				if error_block == 0:
					with open(i, "wb") as file:
						file.write(file_data)
			except:
				error_block += 1

			# Проверка наличия ошибок
			if error_block != 0:
				files_error.append(i)

			# Сброс данных
			error_block = 0
			file_data = None

		end_cryptor_time = datetime.datetime.now()

		return {
			"type": "data",
			"data": {
				"path": path,
				"key_path": key_path,
				"key": key,
				"files_all": files_list,
				"files_error": files_error,
				"time_crypting_sec": (end_cryptor_time - start_cryptor_time).total_seconds(),
				"time_init_sec": (end_time_init - start_time_init).total_seconds()
			}
		}

	def decode_file(self, path: str, key_path: str) -> dict:
		"""Расшифровывает зашифрованные(-ый) файл(ы) и отдаёт словарь с информацией"""
		start_time_init = datetime.datetime.now()
		# Нормализация путей
		path = os.path.abspath(path)
		key_path = os.path.abspath(key_path)

		# Проверка существования
		if os.path.exists(path):
			files_list = __func__.files_in_folder(path)
		else:
			return {"type": "error", "data": "folder_or_file_does_not_exist"}

		# Проверка наличия файлов
		if len(files_list) == 0:
			return {"type": "error", "data": "no_files_found"}

		# Загрузка ключа
		try:
			key = __func__.load_key(key_path)
		except:
			return {"type": "error", "data": "failed_to_load_key_file"}

		# Тестирование ключа
		if not (self.test_key(key)):
			return {"type": "error", "data": "key_file_is_not_working"}

		# Создание переменых для работы
		files_error = []
		error_block = 0
		file_data = None
		if self.speed_mode:
			try:
				farnet = Fernet(key)
				func_decode = __func__.decoding_fernet
			except:
				return {"type": "error", "data": "failed_to_use_speed_mode"}
		else:
			func_decode = __func__.decoding

		end_time_init = datetime.datetime.now()

		# Работа
		start_cryptor_time = datetime.datetime.now()

		for i in files_list:
			# Чтение
			try:
				with open(i, "rb") as file:
					file_data = file.read()
			except:
				error_block += 1

			# Разшифровка
			try:
				if error_block == 0:
					if self.speed_mode:
						file_data = func_decode(farnet, file_data)
					else:
						file_data = func_decode(file_data, key)
			except:
				error_block += 1

			# Запись
			try:
				if error_block == 0:
					with open(i, "wb") as file:
						file.write(file_data)
			except:
				error_block += 1

			# Проверка наличия ошибок
			if error_block != 0:
				files_error.append(i)

			# Сброс данных
			error_block = 0
			file_data = None

		end_cryptor_time = datetime.datetime.now()

		return {
			"type": "data",
			"data": {
				"path": path,
				"key_path": key_path,
				"key": key,
				"files_all": files_list,
				"files_error": files_error,
				"time_crypting_sec": (end_cryptor_time - start_cryptor_time).total_seconds(),
				"time_init_sec": (end_time_init - start_time_init).total_seconds()
			}
		}
	
	def encode_file_with_password(self, path: str, password: str) -> dict:
		"""Зашифровывает файл(ы), `но ключём выступает строка, то есть пароль`, и отдаёт словарь с информацией"""
		start_time_init = datetime.datetime.now()
		# Нормализация путей
		path = os.path.abspath(path)

		# Проверка существования
		if os.path.exists(path):
			files_list = __func__.files_in_folder(path)
		else:
			return {"type": "error", "data": "folder_or_file_does_not_exist"}
		
		# Создание ключа из пароля
		key = __func__.create_key_from_password(password)[1]

		# Тестирование ключа на ошибки при создании
		if not(self.test_key(key)):
			return {"type": "error", "data": "key_file_is_not_working"}

		# Создание переменых для работы
		files_error = []
		error_block = 0
		file_data = None
		if self.speed_mode:
			try:
				farnet = farnet = Fernet(key)
				func_encode = __func__.encoding_fernet
			except:
				return {"type": "error", "data": "failed_to_use_speed_mode"}
		else:
			func_encode = __func__.encoding
		
		end_time_init = datetime.datetime.now()
		
		# Работа
		start_cryptor_time = datetime.datetime.now()

		for i in files_list:
			# Чтение
			try:
				with open(i, "rb") as file:
					file_data = file.read()
			except:
				error_block += 1

			# Зашифровка
			try:
				if error_block == 0:
					if self.speed_mode:
						file_data = func_encode(farnet, file_data)
					else:
						file_data = func_encode(file_data, key)
			except:
				error_block += 1

			# Запись
			try:
				if error_block == 0:
					with open(i, "wb") as file:
						file.write(file_data)
			except:
				error_block += 1

			# Проверка наличия ошибок
			if error_block != 0:
				files_error.append(i)

			# Сброс данных
			error_block = 0
			file_data = None
		
		end_cryptor_time = datetime.datetime.now()

		return {
			"type": "data",
			"data": {
				"path": path,
				"key": key,
				"password": password,
				"files_all": files_list,
				"files_error": files_error,
				"time_crypting_sec": (end_cryptor_time - start_cryptor_time).total_seconds(),
				"time_init_sec": (end_time_init - start_time_init).total_seconds()
			}
		}

	def decode_file_with_password(self, path: str, password: str) -> dict:
		"""Зашифровывает файл(ы), `но ключём выступает строка, то есть пароль`, и отдаёт словарь с информацией"""
		start_time_init = datetime.datetime.now()
		# Нормализация путей
		path = os.path.abspath(path)

		# Проверка существования
		if os.path.exists(path):
			files_list = __func__.files_in_folder(path)
		else:
			return {"type": "error", "data": "folder_or_file_does_not_exist"}
		
		# Создание ключа из пароля
		key = __func__.create_key_from_password(password)[1]

		# Тестирование ключа на ошибки при создании
		if not(self.test_key(key)):
			return {"type": "error", "data": "key_file_is_not_working"}

		# Создание переменых для работы
		files_error = []
		error_block = 0
		file_data = None
		if self.speed_mode:
			try:
				farnet = Fernet(key)
				func_decode = __func__.decoding_fernet
			except:
				return {"type": "error", "data": "failed_to_use_speed_mode"}
		else:
			func_decode = __func__.decoding
		
		end_time_init = datetime.datetime.now()
		
		# Работа
		start_cryptor_time = datetime.datetime.now()

		for i in files_list:
			# Чтение
			try:
				with open(i, "rb") as file:
					file_data = file.read()
			except:
				error_block += 1

			# Зашифровка
			try:
				if error_block == 0:
					if self.speed_mode:
						file_data = func_decode(farnet, file_data)
					else:
						file_data = func_decode(file_data, key)
			except:
				error_block += 1

			# Запись
			try:
				if error_block == 0:
					with open(i, "wb") as file:
						file.write(file_data)
			except:
				error_block += 1

			# Проверка наличия ошибок
			if error_block != 0:
				files_error.append(i)

			# Сброс данных
			error_block = 0
			file_data = None
		
		end_cryptor_time = datetime.datetime.now()

		return {
			"type": "data",
			"data": {
				"path": path,
				"key": key,
				"password": password,
				"files_all": files_list,
				"files_error": files_error,
				"time_crypting_sec": (end_cryptor_time - start_cryptor_time).total_seconds(),
				"time_init_sec": (end_time_init - start_time_init).total_seconds()
			}
		}

	def get_version(self) -> dict:
		"""Отдаёт информацию о версии deCryptorLib"""
		return {
			"name": __info__.name,
			"version": __info__.version,
			"versionint": __info__.versionint,
			"authors": __info__.authors
		}
