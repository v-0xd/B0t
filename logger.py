from colorama import Fore, Style, Back
from datetime import datetime
from threading import Lock
l = Lock()
def write_to_file(file_path, content) -> None:
  with open(file_path, "a") as f:
    f.write(content+'\n')
  
def timestamp() -> str:
  return datetime.now().strftime("%d-%m-20%y %H:%M:%S")

def log(tag:str,content):
  if tag.lower().startswith('s'):
    color = Fore.GREEN
    color2 = Back.GREEN
  elif tag.lower().startswith('e') or tag.lower().startswith('f'):
    color = Fore.RED
    color2 = Back.RED
  elif tag.lower().startswith('w'):
    color = Fore.YELLOW
    color2 = Back.YELLOW
  elif tag.lower().startswith('d') or tag.lower().startswith('i'):
    color = Fore.BLUE if tag.lower().startswith('d') else Fore.CYAN
    color2 = Back.BLUE if tag.lower().startswith('d') else Back.CYAN
  else:
    color = Fore.MAGENTA, color2 = Back.MAGENTA
  time_stamp = timestamp()
  with l:
    print(f"{Style.BRIGHT}{Fore.WHITE}[{Fore.BLACK}time: {Fore.BLUE}{time_stamp}{Fore.WHITE}] [{color}{tag[:3]}{Back.RESET}{Fore.WHITE}] {Fore.GREEN}<*> {Fore.BLACK}{content}{Style.RESET_ALL}")

def inp(content):
  color = Fore.BLUE
  color2 = Back.BLUE
  time_stamp = timestamp()
  with l:
    return input(f"{Style.BRIGHT}{Fore.WHITE}[{Fore.BLACK}time: {color}{time_stamp}{Fore.WHITE}] [{color}INP{Back.RESET}{Fore.WHITE}] {Fore.GREEN}<*> {Fore.BLACK}{content}{Style.RESET_ALL}")