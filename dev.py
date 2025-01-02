import sys
from pathlib import Path

import textfsm
import yaml


def read_text(path: str) -> str:
    with open(path) as f:
        return f.read()


def parse_text(path: str, text: str) -> list:
    with open(path) as f:
        template = textfsm.TextFSM(f)
        result = template.ParseTextToDicts(text)
        return [{key.lower(): value for key, value in d.items()} for d in result]


def write_yaml(path: str, parsed_list: list):
    with open(path, mode="w", encoding="utf-8") as f:
        yaml.safe_dump({"parsed_sample": parsed_list}, f)


def convert_yaml(template_path, raw_path, output_path=None, console=False):
    result = parse_text(template_path, read_text(raw_path))
    if console:
        print(raw_path)
        print(yaml.dump(result))
    if output_path is not None:
        write_yaml(output_path, result)
        print(f"generated: {output_path}")


def generate_yaml_from_file(path: str, write: bool = True):
    input_path = Path(path)
    output_path = input_path.with_suffix(".yml").as_posix()
    command = input_path.parent.name
    vendor = input_path.parent.parent.name
    template_path = f"./templates/{vendor}_{command}.textfsm"

    if write:
        convert_yaml(template_path, path, output_path, False)
    else:
        convert_yaml(template_path, path, None, True)


def generate_yaml_from_dir(path: str, write: bool = True):
    input_path = Path(path)
    command = input_path.name
    vendor = input_path.parent.name
    template_path = f"./templates/{vendor}_{command}.textfsm"
    raw_files = list(input_path.glob("*.raw"))

    for raw_file in raw_files:
        if write:
            output_path = raw_file.with_suffix(".yml").as_posix()
            convert_yaml(template_path, raw_file.as_posix(), output_path, False)
        else:
            convert_yaml(template_path, raw_file.as_posix(), None, True)


def generation_yaml(path: str, write: bool = True):
    input_path = Path(path)
    if input_path.is_file():
        generate_yaml_from_file(path, write)
    else:
        generate_yaml_from_dir(path, write)


def main():
    args = sys.argv
    if len(args) < 2:
        print("subcommand")
        return

    if args[1] == "gen":
        if len(args) == 3:
            generation_yaml(args[2])
        else:
            print("invalid parameter")
    elif args[1] == "conv":
        if len(args) == 3:
            generation_yaml(args[2], False)
        else:
            print("invailed paramater")
    else:
        print("invalid subcommand")


if __name__ == "__main__":
    main()
