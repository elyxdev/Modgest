from pystyle import Write, Colors
from colorama import Fore
import os

ca_main = Fore.LIGHTGREEN_EX
defcol = Colors.cyan_to_green # Main color

def jilog(text:str):
    Write.Print(text, defcol, 0.009)
    print()

def winput(text="", torep=""):
    sarna = Write.Input(text, defcol, 0.009)
    if sarna == "":
        return torep
    else:
        return sarna 

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def remake_string(text: str, max_length: int = 33) -> list:
    lines = []
    while len(text) > max_length:
        # Encuentra el último espacio dentro del límite de longitud
        split_pos = text.rfind(' ', 0, max_length)
        if split_pos == -1:
            # Si no hay un espacio, corta en la longitud máxima
            split_pos = max_length
        lines.append(text[:split_pos].strip())
        text = text[split_pos:].strip()
    lines.append(text)
    return lines

def make_table(table_data: list, table_header="", show=False):
    lines = table_data
    if len(table_header) > 33:
        table_header = remake_string(table_header)
    current_length = 33 # max(len(line) for line in lines if line.strip() != "")
    if show:
        print(f'{ca_main}╔{"═" * (current_length + 2)}╗{Fore.RESET}')
    if table_header != "":
        if type(table_header) == type([]):
            for line in table_header:
                    if show:
                        print(f"{ca_main}║{Fore.RESET} {line} {' ' * (current_length - len(line) -1 )} {ca_main}║")
        else:
            if show:
                print(f"{ca_main}║{Fore.RESET} {table_header} {' ' * (current_length - len(table_header) -1 )} {ca_main}║")
        if show:
            print(f"{ca_main}╠{'═' * (current_length+2)}╣{Fore.RESET}")
    for line in lines:
        if line.strip() == "":
            continue
        padding = current_length - len(line)
        if show:
            print(f'{ca_main}║{Fore.RESET} {line}{" " * padding} {ca_main}║')
    if show:
        print(f'{ca_main}╚{"═" * (current_length + 2)}╝{Fore.RESET}')

    return current_length

if __name__ == "__main__":
    print("Testing tables...")
    longer = make_table(remake_string("Adds plenty of blocks and items to defend and secure your base with."), table_header="[4] security breach objects, blocks, & more open beta")
    print(f"Longest line: {longer}")