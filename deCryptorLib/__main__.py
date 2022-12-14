import time
import deCryptorLib as declib
from rich.console import Console

c = Console()
skw = {"show_locals": True, "word_wrap": True}

password = "Python-3.9.9"

try:
    c.rule("DATA")
    c.print(password.__repr__())
    s1 = time.time()
    c.print(declib.generate_key_from_password(password).__repr__())
    t1 = time.time()-s1
    s2 = time.time()
    c.print(declib.generate_key_from_password(password).__repr__())
    t2 = time.time()-s2
    c.rule("TIME")
    c.print(f"[red]T1[/]: {t1}")
    c.print(f"[red]T2[/]: {t2}")
except:
    c.print_exception(**skw)
