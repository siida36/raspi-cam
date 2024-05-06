"""
MIT License

Copyright (c) 2024 ShoheiIida

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

Author: ShoheiIida
Organization: デジラクダ
"""
from datetime import datetime
from pathlib import Path
from subprocess import run

USER_NAME = "pi"  # TODO: Set your name.
ROOT_DIR = Path(f"/home/{USER_NAME}/raspi-cam")


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d%H-%M-%S")


def logger(msg: str, out_dir: Path, level: str = "[INFO]"):
    cur_time = get_current_time()

    with open(out_dir.joinpath("log"), "a") as f:
        print(f"{cur_time} [{level}]: {msg}", file=f)


def take_photo(out_dir: Path):
    cur_time = get_current_time()
    out_file = out_dir.joinpath(f"image{cur_time}.jpg")

    run(f"fswebcam {out_file}", shell=True)
    logger(f"Take a photo to {out_file}", out_dir)


def flush_history(out_dir: Path, n_max_data: int = 10):
    if len(list(out_dir.glob(".jpg"))) > n_max_data:
        logger("Photos reach max data num, flush photos.", out_dir)
        run(f"rm {out_dir}/*", shell=True)


def main(root_dir: Path = ROOT_DIR):
    """Main routine."""
    out_dir = root_dir.joinpath("output")
    out_dir.mkdir(exist_ok=True, parents=True)

    take_photo(out_dir)
    flush_history(out_dir)


if __name__ == "__main__":
    main()
