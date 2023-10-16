"""
MIT License

Copyright (c) 2023 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import click
import tarfile
import os
import sys
import time
import subprocess
import shlex
from halo import Halo
from tabulate import tabulate
from pathlib import Path

## Docker Build Files
docker_template_file = Path("./Dockerfile.Template")


user_block = "### USER CONFIG ###\n\n### USER CONFIG END ###"


## Helper Functions
def disable_proxy(docker_template):
    return docker_template


def enable_proxy(docker_template):
    return docker_template


def disable_user(docker_template):
    #    chown_line = "COPY --chown=${UNAME}:${GNAME} \\"
    #    docker_template = docker_template.replace(chown_line, "COPY \\")
    docker_template = docker_template.replace(
        "RUN groupadd -r -g", "#RUN groupadd -r -g"
    )
    return docker_template


def set_user(docker_template, uid, gid):
    usr_arg = "ARG UID=1000"
    grp_arg = "ARG GID=1000"
    docker_template = docker_template.replace(usr_arg, f"ARG UID={uid}")
    docker_template = docker_template.replace(grp_arg, f"ARG GID={gid}")
    docker_template = docker_template.replace(
        "#RUN groupadd -r -g", "RUN groupadd -r -g"
    )
    return docker_template


@Halo(text="Creating context", spinner="shark")
def tar_workfolder_context(athena_tool="./athena_tool"):
    out_tar = "athena_tool.tar.gz"
    ath_path = Path(athena_tool)
    with tarfile.open(out_tar, "w:gz") as tar:
        tar.add(ath_path, arcname=os.path.sep)


def pp_val(b):
    if isinstance(b, bool):
        if b:
            return "Yes"
        return "No"
    return b


def create_options_table(option_list, option_names):
    tbl = tabulate([option_list], headers=option_names, tablefmt="fancy_grid")
    tv = tbl.split("\n")

    def blst(va):
        vx = click.style(va, bold=True, fg="blue")
        return vx

    for i in range(0, 3):
        tv[i] = blst(tv[i])
    nv = "\n".join(tv)
    return nv


@click.command()
@click.option("--build", default=False, is_flag=True, help="Build docker image here")
@click.option(
    "--no-user", is_flag=True, help="Do not set a user GID/UID in the Dockerfile"
)
@click.option("--uid", default=1000, help="If setting a user, use this UID")
@click.option(
    "--gid", default=1000, help="If setting a user, use this GID for the user group"
)
@click.option(
    "-f", default=False, is_flag=True, help="Force re-creation of context gzip"
)
@click.option(
    "--version_tag", default=None, help="Version for docker (default is 'latest')"
)
@click.option(
    "--docker_loc", default=None, help="Path to Docker exe (default uses path)"
)
@click.argument("ARGS_OVER", nargs=-1)
def cli(build, no_user, uid, gid, f, version_tag, docker_loc, args_over):
    """
    \b
    Athena Docker Builder Tool
    Configures a Dockerfile and optionally builds it.
    \b

    \b
    Generate a Dockerfile for Athena use. Currently used to
    toggle the SRN proxy options from within the Dockerfile.
    Also allows for overriding the UID for the image.
    \b

    \b
    Args:
      f: Athena code is transported to the Dockerfile as a tar.gz. By default, this script will
         not re-create this file every time the script is run. Set this to force overwrite the tar.gz.
      gid: Override the generated Athena groupID (default is UID 1000)
      uid: Override the Athena userID (default is UID 1000)
      no_user: Use default docker user ID
      proxy: Default is on. Run with --no-proxy to generate a Dockerfile without the
             proxy config (for non-SRN deployment)
    Returns:
      Dockerfile uses to create docker image to run ATHENA container
    \b
    """
    click.secho(f"{'🦉 Athena Setup Tool ':^80}", fg="green", bold=True, underline=True)
    click.echo("\n\n")
    make_dockerfile(proxy=False, no_user=no_user, uid=uid, gid=gid, f=f)
    build_docker(
        build=build, version_tag=version_tag, docker_loc=docker_loc, args_over=args_over
    )


def make_dockerfile(proxy, no_user, uid, gid, f):
    """ """
    status_msg = f"{'🦉 Athena Dockerfile Generation ':^80}"
    opts = ["Proxy?", "Custom User?"]
    vals = [proxy, no_user]
    if not no_user:
        opts.extend(("UserID (o)", "GroupID (o)"))
        vals.append(uid)
        vals.append(gid)
    opts.append("Rebuild?")
    vals.append(f)

    click.secho(
        status_msg,
        fg="bright_blue",
        bold=True,
    )
    click.echo(f'{"Options used for Docker:":^80}')
    click.echo(create_options_table(vals, opts))

    docker_template_data = Path("Dockerfile.Template").read_text()
    if not proxy:
        docker_template_data = disable_proxy(docker_template_data)
    else:
        docker_template_data = enable_proxy(docker_template_data)

    if no_user:
        docker_template_data = disable_user(docker_template_data)
    else:
        docker_template_data = set_user(docker_template_data, uid, gid)

    new_dockerfile = Path("Dockerfile").write_text(docker_template_data)

    if not Path("athena_tool.tar.gz").exists() or f:
        tar_workfolder_context()


def build_docker(build, version_tag, docker_loc, args_over):
    opt_list = ["Tag", "Docker EXE", "Args"]
    doc_cmd = "docker" if docker_loc is None else docker_loc

    version_tag = "latest" if version_tag is None else version_tag

    doc_args = f"build -t athena:{version_tag} {' '.join(args_over)}."
    opt_vals = [version_tag, doc_cmd, args_over]

    msg_hdr = f"{'🦉 Athena Dockerfile Builder 🌳':^80}"
    click.secho(msg_hdr, fg="bright_blue", bold=True)
    click.echo(f'{"Options for build:":^80}')
    click.echo(create_options_table(opt_vals, opt_list))

    if not build:
        sys.exit(click.secho(f"Command is: {doc_cmd} {doc_args}"))
    click.secho("Bulding Athena Docker image...", fg="green")
    with Halo(text="building", spinner="dots") as spin:
        builder = subprocess.run(
            f"{doc_cmd} {doc_args}", shell=True, capture_output=True
        )
        if builder.returncode < 0:
            spin.fail(builder.stderr.decode())


if __name__ == "__main__":
    cli()
