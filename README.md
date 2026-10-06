# Livre
Brechó

## Remoção de fundo das imagens

Script que remove o fundo das fotos de roupas (JPG/PNG) com [`rembg`](https://github.com/danielgatis/rembg) e salva em `output/` com fundo branco puro (#FFFFFF), em PNG sem perda, pronto para Mercado Livre, Shopee e Amazon. A roupa não é alterada.

### Uso

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python remover_fundo.py
```

Opções:

- `--entrada PASTA`: pasta de origem (padrão: `.`)
- `--saida PASTA`: pasta de destino (padrão: `output`)
- `--modelo NOME`: modelo do rembg (padrão: `u2net`; ex.: `isnet-general-use`)
- `--alpha-matting`: bordas mais suaves em franjas e tecidos translúcidos (mais lento)

Na primeira execução o rembg baixa o modelo (~170 MB). Confira o resultado e retoque as bordas se necessário.
