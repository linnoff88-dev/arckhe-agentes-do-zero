#!/usr/bin/env python3
"""Agente do zero (aula 5): modelo + loop + ferramentas + instruções + memória + limites."""
import json, os, sys, urllib.request

MODELO = os.environ.get("MODELO", "llama3.2")
URL = os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"
PASTA = os.path.realpath("trabalho")      # a única pasta que o agente enxerga
MEMORIA = "memoria.json"
MAX_RODADAS = 5                           # o freio: no máximo 5 idas ao modelo por pedido


def cerebro(mensagens, ferramentas):
    corpo = {"model": MODELO, "messages": mensagens, "tools": ferramentas, "stream": False, "think": False,
             "options": {"temperature": 0, "seed": 1}}
    pedido = urllib.request.Request(URL, json.dumps(corpo).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(pedido, timeout=600) as r:
        return json.loads(r.read())["message"]


def dentro(nome):
    caminho = os.path.realpath(os.path.join(PASTA, nome))
    if not caminho.startswith(PASTA + os.sep):
        raise ValueError("fora da pasta de trabalho")
    return caminho


def memorias():
    return json.load(open(MEMORIA)) if os.path.exists(MEMORIA) else []


def ler_arquivo(nome):
    with open(dentro(nome)) as f:
        return f.read()


def escrever_arquivo(nome, texto):
    caminho = dentro(nome)
    if os.path.exists(caminho):           # mexer no que já existe pede OK (sem terminal = não)
        if not sys.stdin.isatty() or input(f"  substituir {nome}? [s/N] ").lower() != "s":
            return "recusado: o dono não aprovou"
    with open(caminho, "w") as f:
        f.write(texto)
    return f"gravado: {nome}"


def lembrar(fato):
    json.dump(memorias() + [fato], open(MEMORIA, "w"), ensure_ascii=False)
    return f"guardado: {fato}"


FERRAMENTAS = {"ler_arquivo": ler_arquivo, "escrever_arquivo": escrever_arquivo, "lembrar": lembrar}
DESCRICOES = [
    {"type": "function", "function": {"name": "ler_arquivo", "description": "Lê um arquivo da pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}}, "required": ["nome"]}}},
    {"type": "function", "function": {"name": "escrever_arquivo", "description": "Grava um arquivo na pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}, "texto": {"type": "string"}},
                    "required": ["nome", "texto"]}}},
    {"type": "function", "function": {"name": "lembrar", "description": "Guarda um fato sobre o dono para sempre.",
     "parameters": {"type": "object", "properties": {"fato": {"type": "string"}}, "required": ["fato"]}}},
]


def responder(pedido, mostrar=print):
    instrucoes = open("instrucoes.md").read()
    lembrancas = "\n".join(f"- {m}" for m in memorias()) or "(nada ainda)"
    mensagens = [{"role": "system", "content": f"{instrucoes}\n\nO que você sabe do dono:\n{lembrancas}"},
                 {"role": "user", "content": pedido}]
    for rodada in range(MAX_RODADAS):
        msg = cerebro(mensagens, DESCRICOES)
        mensagens.append(msg)
        if not msg.get("tool_calls"):
            return msg.get("content", ""), rodada + 1
        for chamada in msg["tool_calls"]:
            nome, args = chamada["function"]["name"], chamada["function"].get("arguments") or {}
            try:
                saida = FERRAMENTAS[nome](**args)
            except Exception as erro:              # ferramenta errada, arquivo que não existe, fora da pasta
                saida = f"recusado: {erro}"
            mostrar(f"[ferramenta] {nome} {json.dumps(args, ensure_ascii=False)} -> {saida[:80]}")
            mensagens.append({"role": "tool", "content": saida})
    return "Parei: cheguei ao limite de rodadas.", MAX_RODADAS


if __name__ == "__main__":
    os.makedirs(PASTA, exist_ok=True)
    resposta, rodadas = responder(" ".join(sys.argv[1:]))
    print(f"{resposta}\n({rodadas} rodada(s))")
