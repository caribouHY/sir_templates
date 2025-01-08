import argparse
from pathlib import Path


import textfsm
import yaml


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_text(path: str, text: str) -> list:
    with open(path) as f:
        template = textfsm.TextFSM(f)
        result = template.ParseTextToDicts(text)
        return [{key.lower(): value for key, value in d.items()} for d in result]


def write_yaml(path: str, parsed_list: list):
    with open(path, mode="w", encoding="utf-8") as f:
        yaml.safe_dump({"parsed_sample": parsed_list}, f)


def convert_yaml(
    template_path: str, raw_path: str, output_path: str = None, console: bool = False
) -> None:
    result = parse_text(template_path, read_text(raw_path))
    if console:
        print(f"Reading {raw_path}")
        print(yaml.dump(result, default_flow_style=False))
    if output_path is not None:
        write_yaml(output_path, result)
        print(f"Generated: {output_path}")


def generate_yaml_from_file(path: str, write: bool = True) -> None:
    input_path = Path(path)
    output_path = input_path.with_suffix(".yml").as_posix()
    command = input_path.parent.name
    vendor = input_path.parent.parent.name
    template_path = f"./templates/{vendor}_{command}.textfsm"

    if write:
        convert_yaml(template_path, path, output_path, False)
    else:
        convert_yaml(template_path, path, None, True)


def generate_yaml_from_dir(path: str, write: bool = True) -> None:
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
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    gen_parser = subparsers.add_parser("gen", help="Generate yaml from file/directory")
    gen_parser.add_argument("path", type=str)

    conv_parser = subparsers.add_parser(
        "conv", help="Convert raw data to yaml (in console)"
    )
    conv_parser.add_argument("path", type=str)

    args = parser.parse_args()

    if args.subcommand == "gen":
        generation_yaml(args.path, True)
    elif args.subcommand == "conv":
        generation_yaml(args.path, False)


if __name__ == "__main__":
    main()
