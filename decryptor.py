import os
import sys
import datetime
from cryptography.fernet import Fernet
# Графичекая библеотека
import rich
from rich.console import Console
from rich.progress import Progress

class _cfg:
	prefix = "\\" if (sys.platform == "win32") else "/"

class _info:
	name = "deCryptor"
	version = "0.5.2-release"
	versionint = 0.52
	author = ", ".join([
		"Роман Слабицкий",
		"Никита Додзин",
		"Марк Метелев",
		"Коломыйцев Алексей"
	])
	company = author
	name_file = os.path.basename(sys.argv[0])

class _text:
	t_version = f"[green]{_info.name}[/] [yellow]v[/][#00ffff]{_info.version}[/] [yellow]([/][#00ffff]{_info.version}[/][yellow])[/] [#bd49bf]от[/] [#ff8800]{_info.company}[/] [#bd49bf]@[/] [#ff8800]{_info.author}[/]" if (
		_info.company != _info.author) else f"[green]{_info.name}[/] [yellow]v[/][#00ffff]{_info.version}[/] [yellow]([/][#00ffff]{_info.versionint}[/][yellow])[/] [#bd49bf]от[/] [#ff8800]{_info.author}[/]"
	t_help = "{0} [blue][MODE][/] [#00eeff]--key[/] [#00ff77]KEY_PATH[/] [green]\"PATH FROM FILE\"[/]\n\nMODE:\n\t[blue]-en[/] - закодировать файл(ов)\n\t[blue]-de[/] - декодирование файл(ов)\n\t[blue]-v[/] или [blue]--version[/] - показывает версию\n\t[blue]-h[/] или [blue]--help[/] - показывает help\nKEY:\n\t[#00eeff]--key[/] [#00ff77]KEY_PATH[/] - путь ко ключу, который открывает доступ к зашифрованому(-ым) файлу(-ам)".format(
		_info.name_file)

class _syntax:
	param = ["-en", "-de"]

class _func:
	def encoding(data: bytes, *, key_path: str = "0.key") -> bytes:
		key = Fernet.generate_key()
		with open(key_path, "wb") as file:
			file.write(key)
		criptor = Fernet(key)
		return criptor.encrypt(data)

	def decoding(data: bytes, *, key_path: str = "0.key") -> bytes:
		with open(key_path, "rb") as file:
			key = file.read()
		criptor = Fernet(key)
		return criptor.decrypt(data)

	def files_in_folder(folderpath: str = "."):
		files = []
		if not(os.path.isfile(folderpath)):
			for i in os.listdir(folderpath):
				path = os.path.abspath(
					folderpath + "\\" if (sys.platform == "win32") else "/" + i)
				if os.path.isdir(path):
					for ii in _func.files_in_folder(path):
						files.append(ii)
				else:
					files.append(path)
		else:
			path = os.path.abspath(
				folderpath + "\\" if (sys.platform == "win32") else "/" + i)
			files.append(path)
		return files

class _tmp:
	key = "0.key"
	data = None
	dataout = None

console = Console()

if len(sys.argv) >= 3:
	if str(sys.argv[1]) in _syntax.param:
		if os.path.exists(str(sys.argv[len(sys.argv) - 1])):
			try:
				if str(sys.argv[1]) == _syntax.param[0]:
					files_list = _func.files_in_folder(
						str(sys.argv[len(sys.argv) - 1]))
					if len(files_list) > 0:
						time_start = datetime.datetime.now()
						if "--key" in sys.argv:
							try:
								_tmp.key = str(
									sys.argv[sys.argv.index("--key") + 1])
							except:
								_tmp.key = "0.key"
						with Progress() as progress:
							TaskEncoding = progress.add_task(
								"[green]Закодирование...", total=3 * len(files_list))
							for i in files_list:
								try:
									with open(i, "rb") as file:
										_tmp.data = file.read()
								except:
									console.print_exception()
								progress.update(TaskEncoding, advance=1)
								try:
									_tmp.dataout = _func.encoding(_tmp.data, key_path=os.path.split(
										os.path.abspath(str(sys.argv[len(sys.argv) - 1])))[0] + _cfg.prefix + _tmp.key)
								except:
									console.print_exception()
									_tmp.dataout = _tmp.data
								progress.update(TaskEncoding, advance=1)
								try:
									with open(i, "wb") as file:
										file.write(_tmp.dataout)
								except:
									console.print_exception()
								progress.update(TaskEncoding, advance=1)

						time_end = datetime.datetime.now()
						console.print("[blue]Заняло времени[/]:",
									  time_end - time_start)
					else:
						console.print("[red]Ошибка[/]: файл(ы) не найден(ы)")
				else:
					files_list = _func.files_in_folder(
						str(sys.argv[len(sys.argv) - 1]))
					if os.path.exists(os.path.split(os.path.abspath(str(sys.argv[len(sys.argv) - 1])))[0] + _cfg.prefix + _tmp.key):
						if len(files_list) > 0:
							time_start = datetime.datetime.now()
							if "--key" in sys.argv:
								try:
									_tmp.key = str(
										sys.argv[sys.argv.index("--key") + 1])
								except:
									_tmp.key = "0.key"
							with Progress() as progress:
								TaskDecoding = progress.add_task(
									"[green]Декодирование...", total=3 * len(files_list))
								for i in files_list:
									try:
										with open(i, "rb") as file:
											_tmp.data = file.read()
									except:
										pass
										# console.print_exception()
									progress.update(TaskDecoding, advance=1)
									try:
										_tmp.dataout = _func.decoding(_tmp.data, key_path=os.path.split(
											os.path.abspath(str(sys.argv[len(sys.argv) - 1])))[0] + _cfg.prefix + _tmp.key)
									except:
										pass
										# console.print_exception()
										_tmp.dataout = _tmp.data
									progress.update(TaskDecoding, advance=1)
									try:
										with open(i, "wb") as file:
											file.write(_tmp.dataout)
									except:
										pass
										# console.print_exception()
									progress.update(TaskDecoding, advance=1)

							time_end = datetime.datetime.now()
							console.print(
								"[blue]Заняло времени[/]:", time_end - time_start)
						else:
							console.print(
								"[red]Ошибка[/]: файл(ы) не найден(ы)")
					else:
						console.print(
							"[red]Ошибка[/]: указаного ключа не существует")
			except:
				console.print("[red]Ошибка[/]: Критическая ошибка")
				# console.print_exception()
		else:
			console.print(
				"[red]Ошибка[/]: Файл [yellow]\"{0}\"[/] не существует".format(sys.argv[2]))
	else:
		console.print(
			"[red]Ошибка[/]: Неизвестный параметр [yellow]\"{0}\"[/]".format(sys.argv[1]))
else:
	if len(sys.argv) >= 2:
		if str(sys.argv[1]) in ("-v", "--version"):
			console.print(_text.t_version)
		else:
			if str(sys.argv[1]) in ("-h", "--help"):
				console.print(_text.t_help)
			else:
				console.print(_text.t_help)
	else:
		console.print(_text.t_version)
		console.print(_text.t_help)
