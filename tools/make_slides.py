import pathlib
import shutil
import subprocess
import sys
from typing import List, Optional


def build_file(
    tex_file: pathlib.Path, out_dir: Optional[pathlib.Path] = None
) -> pathlib.Path:
    options = [
        "-cd",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-halt-on-error",
        "-shell-escape",
        "-lualatex",
    ]
    if out_dir is not None:
        options.append(f"-output-directory={out_dir.resolve()}")
        pdf_path = out_dir / f"{tex_file.stem}.pdf"
    else:
        pdf_path = tex_file.with_suffix(".pdf")
    subprocess.run(
        [
            "latexmk",
            *options,
            str(tex_file),
        ]
    )
    return pdf_path


def main(args: List[str] = sys.argv[1:]):
    if len(args) == 1:
        repo_root = pathlib.Path(args[0])
    elif not args:
        repo_root = pathlib.Path(__file__).parent.parent
    else:
        raise ValueError("Wrong number of args")

    out_dir = repo_root / "_build"
    out_dir.mkdir(exist_ok=True)

    for slide_tex in repo_root.glob("slides/lecture*/lecture*.tex"):
        pdf_file = build_file(slide_tex)
        shutil.copy(str(pdf_file), out_dir)


if __name__ == "__main__":
    main()