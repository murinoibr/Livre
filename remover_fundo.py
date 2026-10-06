#!/usr/bin/env python3
"""Remove o fundo das imagens de roupas e salva com fundo branco (#FFFFFF) em output/."""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

EXTENSOES = {".jpg", ".jpeg", ".png"}
IGNORAR = {".git", "output", "venv", ".venv", "node_modules"}


def listar_imagens(raiz: Path, saida: Path):
    for caminho in sorted(raiz.rglob("*")):
        partes = set(caminho.relative_to(raiz).parts[:-1])
        if partes & IGNORAR or saida in caminho.parents:
            continue
        if caminho.is_file() and caminho.suffix.lower() in EXTENSOES:
            yield caminho


def processar(caminho: Path, raiz: Path, saida: Path, sessao, alpha_matting: bool):
    from rembg import remove

    with Image.open(caminho) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
    recorte = remove(img, session=sessao, alpha_matting=alpha_matting)
    fundo = Image.new("RGBA", recorte.size, (255, 255, 255, 255))
    fundo.alpha_composite(recorte.convert("RGBA"))
    destino = (saida / caminho.relative_to(raiz)).with_suffix(".png")
    destino.parent.mkdir(parents=True, exist_ok=True)
    fundo.convert("RGB").save(destino, format="PNG", optimize=True)
    return destino


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--entrada", default=".", help="pasta com as imagens (padrão: .)")
    p.add_argument("--saida", default="output", help="pasta de saída (padrão: output)")
    p.add_argument("--modelo", default="u2net", help="modelo rembg (padrão: u2net)")
    p.add_argument("--alpha-matting", action="store_true",
                   help="suaviza bordas (franjas, transparências); mais lento")
    args = p.parse_args()

    raiz = Path(args.entrada).resolve()
    saida = Path(args.saida).resolve()
    imagens = list(listar_imagens(raiz, saida))
    if not imagens:
        print("Nenhuma imagem JPG/PNG encontrada.")
        return 0

    from rembg import new_session

    sessao = new_session(args.modelo)
    erros = 0
    for i, img in enumerate(imagens, 1):
        try:
            destino = processar(img, raiz, saida, sessao, args.alpha_matting)
            print(f"[{i}/{len(imagens)}] {img.name} -> {destino}")
        except Exception as e:
            erros += 1
            print(f"[{i}/{len(imagens)}] ERRO em {img.name}: {e}", file=sys.stderr)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
