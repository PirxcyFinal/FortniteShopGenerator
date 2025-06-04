import os
import crayons
import survey

from typing import Any

logo: Any = crayons.red("""                                
                                
       o                        
    _      ,_         __        
  |/ \_|  /  |  /\/  /    |   | 
  |__/ |_/   |_/ /\_/\___/ \_/|/
 /|                          /| 
 \|                          \| 
""")

def cls() -> None:
    """
    Clears the console screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def center(var: str, space: int | None = None) -> str:
    """
    Centers a string in the console.
    """
    if not space:
        space = (
            os.get_terminal_size().columns
            - len(var.splitlines()[int(len(var.splitlines()) / 2)])
        ) // 2
    return "\n".join((" " * int(space)) + var for var in var.splitlines())


def generate_menu(options: dict[Any, Any], text: str) -> Any:
    """
    Generates a menu to pirxcy's liking.
    """

    cls()
    print(center(logo))  # type: ignore

    index: int = survey.routines.select(  # type: ignore
        text,
        options=list(options.keys()),
        focus_mark="➤  ",
        evade_color=survey.colors.basic("red"),
    )

    command = list(options.values())[index]
    return command
