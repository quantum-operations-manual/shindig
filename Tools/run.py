import argparse
import sys
import ue


def parse_args():
    parser = argparse.ArgumentParser("UE4 Runner")
    subparsers = parser.add_subparsers()

    generate_parser = subparsers.add_parser("generate", help="Generate project files")
    generate_parser.set_defaults(action=generate_files)
    compile_parser = subparsers.add_parser("compile", help="Compile the game module")
    compile_parser.add_argument('--platform', default='Win64', help="Which platform to compile for")
    compile_parser.add_argument('--config', default='Development', help="Which configuration to compile")
    compile_parser.set_defaults(action=compile_ue)
    open_parser = subparsers.add_parser('launch', help="Open the editor")
    open_parser.set_defaults(action=open_ue)
    parser.add_argument('project_name', default="Shindig", help="Name of the UE4 project")
    return parser.parse_args()

def generate_files(args):
    ue.generate_project_files(args.project_name)

def compile_ue(args):
    ue.compile_game(args.project_name, args.platform, args.config)

def open_ue(args):
    ue.start_editor(args.project_name)

def main():
    args = parse_args()
    args.action(args)

if __name__ == "__main__":
    sys.exit(main())