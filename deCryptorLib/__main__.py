import time
import random
import string
import deCryptorLib as declib
from rich.console import Console

c = Console()
dc = declib.deCryptor()
skw = {"show_locals": True, "word_wrap": True}
pr = list(string.printable)
tests = 4096

def genpass(length: int=16) -> str:
    return "".join([random.choice(pr) for i in range(length)])

try:
    c.rule("TESTS", characters="*")
    ss = []
    for i in range(tests):
        s = time.time() ; key = dc.key_from_text(ps:=genpass()) ; t = time.time()-s
        c.print(f"[red]T({i+1}/{tests})[/]: {ps.__repr__()} [yellow]->[/] {key.__repr__()} | [blue]Time[/] ([yellow]sec[/]): {t:.3f}")
        ss.append(t)
    c.rule("Timers", characters="*")
    c.print(f"[blue]Average time[/] ([yellow]sec[/]): {sum(ss)/len(ss):.3f}")
    c.print(f"[green]Total time[/] ([yellow]sec[/]): {sum(ss):.3f}")
    c.rule("Done!", characters="*")
except:
    c.print_exception(**skw)
