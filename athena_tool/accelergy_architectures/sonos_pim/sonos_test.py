#!/usr/bin/env python3
from pathlib import Path

from typing import Optional, List
import typer
import subprocess

# GLOBAL CLI OPTIONS#
TIMELOOP_MAPPER_PATH = None
SONOS_FOLDER = "./"


def check_path(path: Path, ptype: str = ".yaml", is_dict: bool = False):
    if path.exists():
        if is_dict and path.is_dir():
            return True
        if ptype in str(path):
            return True
    return False


def check_paths(path_list: List[Path], ptype: str = ".yaml"):
    path_check = [check_path(p, ptype) for p in path_list]
    return path_check


def f_t_s(paths, abs=False):
    if not isinstance(paths, list):
        paths = [paths]
    if abs:
        path_s = [str(p.absolute()) for p in paths]
    else:
        path_s = [str(p) for p in paths]
    return path_s


# @click.command()
# @click.option('--arch-yaml', '-a', help='Architecture YAML file', default='arch/sonos_tile.yaml')
# @click.option('--no-constraints', is_flag=True, default=False, help='use constraints file')
# @click.option('--constraint_ovr', '-c', help='constraint yaml override', default=None)
def test_arch(
    timeloop_mapper: Path,
    arch_yaml: Path = Path("arch/sonos_tile.yaml"),
    no_constraints: bool = typer.Option(False, "--no-constraints"),
    constraint_ovr: Optional[List[Path]] = typer.Option(None),
    do_abs: bool = typer.Option(False, "--do_abs"),
    problem_file: Path = Path("vgg/vgg_layer1.yaml"),
    sonos_dir: Path = Path("./"),
):
    use_constraints = not no_constraints
    global SONOS_FOLDER
    global TIMELOOP_MAPPER_PATH
    problem_file = sonos_dir / problem_file
    arch_yaml = sonos_dir / arch_yaml

    # sonos_dir = Path(SONOS_FOLDER)
    const_files = []
    typer.secho(f"{use_constraints=}", fg="green")
    if use_constraints:
        typer.secho(f"Constraint Overrides: {constraint_ovr}", fg="green")
        if not constraint_ovr:
            const_file = sonos_dir / "constraints/constraints.yaml"
            const_files.append(const_file)
        else:
            for co in constraint_ovr:
                print(co)
                co = sonos_dir / co
                print(f"Fixed co: {co}")
                if co.is_dir():
                    for const_file in co.rglob("*.yaml"):
                        const_files.append(const_file)
                else:
                    const_files.append(co)

        typer.secho(f"{const_files=}", fg="blue")

    arch_files = []
    comp_folder = arch_yaml.parent / "components/"
    # for f in (sonos_dir / 'arch/components/').rglob("*.yaml"):
    for f in comp_folder.rglob("*.yaml"):
        arch_files.append(f)

    mapper_file = sonos_dir / "mapper/mapper.yaml"

    # problem_file = sonos_dir / 'vgg/vgg_layer1.yaml'

    # arch_files = [str(f) for f in arch_files]
    arch_files = f_t_s(arch_files, do_abs)
    const_file = " ".join(f_t_s(const_files, do_abs))
    timeloop_mapper = " ".join(f_t_s(timeloop_mapper, do_abs))
    arch_yaml = " ".join(f_t_s(arch_yaml, do_abs))
    problem_file = " ".join(f_t_s(problem_file, do_abs))

    tl_mapper_args = f'{timeloop_mapper} {arch_yaml}  {" ".join(arch_files)} {const_file} {mapper_file} {problem_file} '
    print(tl_mapper_args)
    subprocess.run(tl_mapper_args, shell=True)


if __name__ == "__main__":
    typer.run(test_arch)
