import PySimpleGUI as sg
import deCryptorLib
import os
from collections import namedtuple

# Инициализация нужного для работы
DeCryptor = deCryptorLib.deCryptor() # Это мой обрабочик, в который задаёшь путь к терминальной версии deCryptor, даже EXE можно он всё сам обработает
path = str()                         # Это путь к папке или файлу (для последущего закодирования или раз кодирования)
key = str()                          # Это путь к ключу (даже если он не указан будет работать)

# Функции
def encoding(p: str, key_path: str=None) -> dict:
	return DeCryptor.encode(p, key_path)


def decoding(p: str, key_path: str) -> dict:
	return DeCryptor.decode(p, key_path)

def named_tuple(name: str, data: dict) -> namedtuple:
	return namedtuple(name, data.keys())(*data.values())

# Получение информации
__info_core__ = named_tuple("info_core", DeCryptor.get_version())
__info_gui__ = named_tuple("info_gui", {"name": "deCryptor GUI", "version": "0.1-release", "versionint": 0.1})

# Окно программы
layout = [
	[
		sg.Text("Путь к файлу:"),
		sg.InputText(key="path"),
		sg.FolderBrowse(target="path"),
		[
			sg.Radio("Зашифровать", 1, key="encode_radio", default=True),
			sg.Radio("Расшифровать", 1, key="decode_radio", default=False)
		],
	],
	[
		sg.Text("Путь к ключу (необезательно):"),
		sg.InputText(key="key_path"),
		sg.FileBrowse(target="key_path")
	],
	[sg.Output(size=(88, 20), key="OutputConsole")],
	[sg.Submit("Запуск", key="Start"), sg.Cancel("Очистить логи", key="ClearConsole"), sg.Text("Версия ядра: {0} ({1})\nВерсия GUI: {2} ({3})".format(__info_core__.version, __info_core__.versionint, __info_gui__.version, __info_gui__.versionint), justification="left")]
]

# Создание окна
window = sg.Window("{0}".format(__info_gui__.name), layout)

# Включения проверки нажатий
while True:  # The Event Loop
	event, values = window.read()
	# print(event, values) #debug

	if event in (None, "Exit", "Cancel"):
		break

	if event == "ClearConsole":
		window["OutputConsole"].update(value="")

	if event == "Start":
		path = window["path"].get().replace("/", os.sep)

		if window["encode_radio"].get():
			print("{0} Начало зашифровки {0}".format("-"*8))
			key = window["key_path"].get().replace("/", os.sep)

			if not((key == "") or (len(key) < 3)):
				result = encoding(path, key_path=key)
			else:
				result = encoding(path)
			
			if result["type"] == "error":
				text_out = "Ошибка: " + result["data"].replace("_", " ")
			elif result["type"] == "data":
				text_out = "Путь к ключу: {0}\n\n".format(result["data"]["key_path"])
				if len(result["data"]["files_error"]) != 0:
					text_out += "Найден(о) {0} файл(ов), из них неудачными оказались:\n".format(len(result["data"]["files_all"]))
					for i in result["data"]["files_all"]:
						text_out += "- " + i + "\n"
				else:
					text_out += "Все найден(ые) {0} файл(а), удалось зашифровать!\n".format(len(result["data"]["files_all"]))
				text_out += "\nВыполнено за {0} секунд(у)".format(round(result["data"]["time_crypting_sec"] + result["data"]["time_init_sec"], 4))
			print(text_out)
			print("{0} Конец зашифровки {0}\n".format("-"*8))

		elif window["decode_radio"].get():
			print("{0} Начало расшифровки {0}".format("-"*8))
			key = window["key_path"].get().replace("/", os.sep)
			if (key == "") or (len(key) < 3):
				result = {"type": "error", "data": "key_not_specified"}
			else:
				result = decoding(path, key_path=key)

			if result["type"] == "error":
				text_out = "Ошибка: " + result["data"].replace("_", " ")
			elif result["type"] == "data":
				text_out = "Путь к ключу: {0}\n\n".format(result["data"]["key_path"])
				if len(result["data"]["files_error"]) != 0:
					text_out += "Найден(о) {0} файл(ов), из них неудачными оказались:\n".format(len(result["data"]["files_all"]))
					for i in result["data"]["files_all"]:
						text_out += "- " + i + "\n"
				else:
					text_out += "Все найден(ые) {0} файл(а), удалось расшифровать!\n".format(len(result["data"]["files_all"]))
				text_out += "\nВыполнено за {0} секунд(у)".format(round(result["data"]["time_crypting_sec"] + result["data"]["time_init_sec"], 4))
			print(text_out)
			print("{0} Конец расшифровки {0}\n".format("-"*8))
			
