import os
import sys

class HandlerDict():
    def __init__(self, decpyptor_path: str, *, python_path: str=None) -> None:
        self.decpyptor_path = os.path.abspath(decpyptor_path)
        if python_path == None:
            self.command_start = (("python " if (sys.platform == "win32") else "python3 ") if (os.path.splitext(self.decpyptor_path)[0] == ".py") else "") + self.decpyptor_path
        else:
            self.command_start = (python_path if (os.path.splitext(self.decpyptor_path)[0] == ".py") else "") + self.decpyptor_path

    def start(self, path: str, mode: str, *, key_path: str=None) -> dict:
        """Парсит dict информацию из deCryptor"""
        cmdl_argv = [mode, "--dict"]
        if key_path != None:
            cmdl_argv.append("--key \"" + key_path + "\"")
        cmdl_argv.append("\"" + path + "\"")
        return eval(os.popen("{0} {1}".format(self.command_start, " ".join(cmdl_argv))).read().split("\n")[1])

    def get_info(self) -> dict:
        """Отдаёт dict с информацией о программе"""
        return eval(os.popen("{0} --version --dict".format(self.command_start)).read().split("\n")[1])