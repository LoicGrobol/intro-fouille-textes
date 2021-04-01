import pathlib
import re
import sys
from typing import Iterable, List, Optional

import wikipedia


def cleanup(text: str, keywords: Optional[Iterable[str]] = None) -> str:
    text = re.sub("\n+", "\n", text)
    text = re.sub(r"=*=\s*", "", text)
    if keywords is not None:
        for w in keywords:
            text = re.sub(fr"{w}\w*\s*", "", text, flags=re.IGNORECASE)
    return text


def get_docs(
    req: str, out_dir: pathlib.Path, n_docs: int = 16, n_lines: int = -1
) -> List[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    scrapped = []
    docs = wikipedia.search(req, results=n_docs)
    for i, page_title in enumerate(docs):
        print(f"Processing {page_title}", file=sys.stderr)
        try:
            page = wikipedia.page(page_title)
        except wikipedia.DisambiguationError as e:
            page = wikipedia.page(e.options[0])
        scrapped.append(page.url)
        with open(out_dir / f"doc{i}.txt", "w") as out_stream:
            cleaned_text = cleanup(page.content, keywords=[req])
            text = "\n".join(cleaned_text.splitlines()[:n_lines])
            out_stream.write(text)
    return scrapped


def main(args: List[str] = sys.argv[1:]):
    if len(args) == 1:
        repo_root = pathlib.Path(args[0])
    elif not args:
        repo_root = pathlib.Path(__file__).parent.parent
    else:
        raise ValueError("Wrong number of args")

    out_dir = repo_root / "data" / "expl3"
    out_dir.mkdir(exist_ok=True)

    scrapped = []
    wikipedia.set_lang("fr")
    scrapped.extend(get_docs("culture", out_dir=out_dir / "culture", n_lines=64))
    scrapped.extend(get_docs("société", out_dir=out_dir / "société", n_lines=64))

    with open(out_dir / "page_urls.lst", "w") as out_stream:
        for p in scrapped:
            out_stream.write(f"{p}\n")


if __name__ == "__main__":
    main()