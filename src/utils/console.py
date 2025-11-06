from rich import print


def rich_input(prompt: str) -> str:
    print(prompt, end="")
    return input()


def ask_confirmation(prompt: str) -> bool:
    full_prompt = f"[yellow]CONFIRM[/yellow] >>> {prompt} (Y/n): "
    while True:
        response = rich_input(full_prompt).strip()
        if response.lower() in ("y", "yes", ""):
            return True
        elif response.lower() in ("n", "no"):
            return False
