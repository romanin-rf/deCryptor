import os
import sys
import datetime
from cryptography.fernet import Fernet

# Графичекая библеотека
from rich.console import Console
from rich.progress import Progress


class _cfg:
	prefix = "\\" if (sys.platform == "win32") else "/"


class _info:
	name = "deCryptor"
	version = "0.5.4-release"
	versionint = 0.54
	author = ", ".join(
		["Роман Слабицкий", "Никита Додзин", "Марк Метелев", "Коломыйцев Алексей"]
	)
	company = author
	name_file = os.path.basename(sys.argv[0])


class _text:
	t_version = (
		f"[green]{_info.name}[/] [yellow]v[/][#00ffff]{_info.version}[/] [yellow]([/][#00ffff]{_info.version}[/][yellow])[/] [#bd49bf]от[/] [#ff8800]{_info.company}[/] [#bd49bf]@[/] [#ff8800]{_info.author}[/]"
		if (_info.company != _info.author)
		else f"[green]{_info.name}[/] [yellow]v[/][#00ffff]{_info.version}[/] [yellow]([/][#00ffff]{_info.versionint}[/][yellow])[/] [#bd49bf]от[/] [#ff8800]{_info.author}[/]"
	)
	t_help = '{0} [blue][MODE][/] [#00eeff]--key[/] [#00ff77]KEY_PATH[/] [#f03a85]--dict[/] [green]"PATH FROM FILE"[/]\n\nMODE:\n\t[blue]-en[/] - закодировать файл(ов)\n\t[blue]-de[/] - декодирование файл(ов)\n\t[blue]-v[/] или [blue]--version[/] - показывает версию\n\t[blue]-h[/] или [blue]--help[/] - показывает help\nKEY:\n\t[#00eeff]--key[/] [#00ff77]KEY_PATH[/] - путь ко ключу, который открывает доступ к зашифрованому(-ым) файлу(-ам)\nJSON:\n\t[#f03a85]--dict[/] - это необезательный параметр, выводит информацию в виде [green]dict[/]'.format(
		_info.name_file
	)


class _syntax:
	parameters = {
		"key": "--key",
		"encoding": "-en",
		"decoding": "-de",
		"version": ["-v", "--version"],
		"help": ["-h", "--help"],
		"debag": "--debag",
		"json": "--dict",
	}


class _func:
	def encoding(data: bytes, key_path: str) -> bytes:
		key = Fernet.generate_key()
		with open(key_path, "wb") as file:
			file.write(key)
		criptor = Fernet(key)
		return criptor.encrypt(data)

	def decoding(data: bytes, key_path: str) -> bytes:
		with open(key_path, "rb") as file:
			key = file.read()
		criptor = Fernet(key)
		return criptor.decrypt(data)

	def files_in_folder(folderpath: str) -> list:
		files = []
		folder_abspath = os.path.abspath(folderpath)
		if os.path.isdir(folder_abspath):
			for i in os.listdir(folder_abspath):
				path = folder_abspath + os.sep + i
				if os.path.isdir(path):
					for _i in _func.files_in_folder(path):
						files.append(_i)
				elif os.path.isfile(path):
					files.append(path)
		elif os.path.isfile(folder_abspath):
			files.append(folder_abspath)
		return files


class _tmp:
	key = "0.key"
	data = None
	dataout = None
	debag = True if (_syntax.parameters["debag"] in sys.argv) else False
	json_out = not (
		(True if (_syntax.parameters["json"] in sys.argv) else False)
		if (not (debag))
		else False
	)
	error_files = []
	count_error = 0


console = Console()

if len(sys.argv) >= 3:
	if sys.argv[1] in _syntax.parameters.values():
		if os.path.exists(sys.argv[len(sys.argv) - 1]):
			try:
				if sys.argv[1] == _syntax.parameters["encoding"]:

					files_list = _func.files_in_folder(sys.argv[len(sys.argv) - 1])

					if len(files_list) > 0:

						time_start = datetime.datetime.now()

						if _syntax.parameters["key"] in sys.argv:
							try:
								_tmp.key = sys.argv[
									sys.argv.index(_syntax.parameters["key"]) + 1
								]
							except:
								console.print_exception() if (_tmp.debag) else None
								_tmp.key = "0.key"

						with Progress() as progress:
							TaskEncoding = progress.add_task(
								"[green]Закодирование...", total=3 * len(files_list)
							)

							for i in files_list:
								try:
									with open(i, "rb") as file:
										_tmp.data = file.read()
								except:
									console.print_exception() if (_tmp.debag) else None
									_tmp.count_error += 1

								progress.update(TaskEncoding, advance=1)

								try:
									_tmp.dataout = _func.encoding(
										_tmp.data,
										key_path=os.path.split(
											os.path.abspath(sys.argv[len(sys.argv) - 1])
										)[0]
										+ _cfg.prefix
										+ _tmp.key,
									)
								except:
									console.print_exception() if (_tmp.debag) else None
									_tmp.count_error += 1
									if _tmp.data != None:
										_tmp.dataout = _tmp.data

								progress.update(TaskEncoding, advance=1)

								try:
									if _tmp.data != None:
										with open(i, "wb") as file:
											file.write(_tmp.dataout)
								except:
									console.print_exception() if (_tmp.debag) else None
									_tmp.count_error += 1

								if _tmp.count_error > 0:
									_tmp.error_files.append(i)

								_tmp.data = None
								_tmp.dataout = None
								_tmp.count_error = 0

								progress.update(TaskEncoding, advance=1)

						time_end = datetime.datetime.now()

						print()
						console.print(
							"[blue]Заняло времени[/]: {0}".format(
								(time_end - time_start)
							)
						) if (_tmp.json_out) else print(
							"{0}".format(
								{
									"type": "data",
									"data": {
										"keypath": _tmp.key,
										"files_all": files_list,
										"files_error": _tmp.error_files,
										"time": (time_end - time_start).total_seconds(),
									},
								}
							)
						)
					else:
						print()
						console.print("[red]Ошибка[/]: файл(ы) не найден(ы)") if (
							_tmp.json_out
						) else print(
							"{0}".format({"type": "error", "data": "not_found"})
						)

				elif sys.argv[1] == _syntax.parameters["decoding"]:

					files_list = _func.files_in_folder(sys.argv[len(sys.argv) - 1])

					if len(files_list) > 0:

						time_start = datetime.datetime.now()

						if _syntax.parameters["key"] in sys.argv:
							try:
								_tmp.key = sys.argv[
									sys.argv.index(_syntax.parameters["key"]) + 1
								]
							except:
								console.print_exception() if (_tmp.debag) else None
								_tmp.key = "0.key"

						with Progress() as progress:
							TaskEncoding = progress.add_task(
								"[green]Закодирование...", total=3 * len(files_list)
							)

							for i in files_list:
								try:
									with open(i, "rb") as file:
										_tmp.data = file.read()
								except:
									console.print_exception() if (_tmp.debag) else None
									_tmp.count_error += 1

								progress.update(TaskEncoding, advance=1)

								try:
									_tmp.dataout = _func.decoding(
										_tmp.data,
										key_path=os.path.split(
											os.path.abspath(sys.argv[len(sys.argv) - 1])
										)[0]
										+ _cfg.prefix
										+ _tmp.key,
									)
								except:
									console.print_exception() if (_tmp.debag) else None
									_tmp.count_error += 1
									if _tmp.data != None:
										_tmp.dataout = _tmp.data

								progress.update(TaskEncoding, advance=1)

								try:
									if _tmp.data != None:
										with open(i, "wb") as file:
											file.write(_tmp.dataout)
								except:
									console.print_exception() if (_tmp.debag) else None
									_tmp.count_error += 1

								if _tmp.count_error > 0:
									_tmp.error_files.append(i)

								_tmp.data = None
								_tmp.dataout = None
								_tmp.count_error = 0

								progress.update(TaskEncoding, advance=1)

						time_end = datetime.datetime.now()

						print()
						console.print(
							"[blue]Заняло времени[/]: {0}".format(
								(time_end - time_start)
							)
						) if (_tmp.json_out) else print(
							"{0}".format(
								{
									"type": "data",
									"data": {
										"keypath": _tmp.key,
										"files_all": files_list,
										"files_error": _tmp.error_files,
										"time": (time_end - time_start).total_seconds(),
									},
								}
							)
						)
					else:
						print()
						console.print("[red]Ошибка[/]: файл(ы) не найден(ы)") if (
							_tmp.json_out
						) else print(
							"{0}".format(
								{"type": "error", "data": "files_is_not_found"}
							)
						)

				elif sys.argv[1] in _syntax.parameters["version"]:
					console.print(_text.t_version)
				elif sys.argv[1] in _syntax.parameters["help"]:
					console.print(_text.t_help)
				else:
					console.print(_text.t_version)
					print()
					console.print(_text.t_help)
			except:
				print()
				console.print_exception() if (_tmp.debag) else (
					print("{0}".format({"type": "error", "data": "critical"}))
					if (_tmp.json_out)
					else console.print("[red]Ошибка[/]: Критическая ошибка")
				)
		else:
			print()
			console.print(
				'[red]Ошибка[/]: Файл или папки [yellow]"{0}"[/] не существует'.format(
					sys.argv[len(sys.argv) - 1]
				)
			) if (_tmp.json_out) else print(
				"{0}".format({"type": "error", "data": "files_or_folder_is_not_found"})
			)
	else:
		print()
		console.print(
			'[red]Ошибка[/]: Неизвестный параметр [yellow]"{0}"[/]'.format(sys.argv[1])
		) if (_tmp.json_out) else print(
			"{0}".format({"type": "error", "data": "unknown_parameter"})
		)
else:
	if len(sys.argv) >= 2:
		if sys.argv[1] in _syntax.parameters["version"]:
			console.print(_text.t_version)
		elif sys.argv[1] in _syntax.parameters["help"]:
			console.print(_text.t_help)
		else:
			console.print(_text.t_version)
			print()
			console.print(_text.t_help)
	else:
		console.print(_text.t_version)
		print()
		console.print(_text.t_help)
