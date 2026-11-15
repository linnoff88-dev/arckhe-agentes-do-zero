#!/usr/bin/env python3
"""Agente do zero (aula 4): + instruções num arquivo e memória que fica entre uma conversa e outra."""
import json, os, sys, urllib.request

MODELO = os.environ.get("MODELO", "llama3.2")
URL = os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"
PASTA = os.path.realpath("trabalho")
MEMORIA = "memoria.json"
MAX_RODADAS = 5


def cerebro(mensagens, ferramentas):
    corpo = {"model": MODELO, "messages": mensagens, "tools": ferramentas, "stream": False, "think": False,
             "options": {"temperature": 0, "seed": 1}}
    pedido = urllib.request.Request(URL, json.dumps(corpo).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(pedido, timeout=600) as r:
        return json.loads(r.read())["message"]


def memorias():
    return json.load(open(MEMORIA)) if os.path.exists(MEMORIA) else []


def ler_arquivo(nome):
    with open(os.path.join(PASTA, nome)) as f:      # ainda sem trava: ela entra na aula 5
        return f.read()


def lembrar(fato):
    json.dump(memorias() + [fato], open(MEMORIA, "w"), ensure_ascii=False)
    return f"guardado: {fato}"


FERRAMENTAS = {"ler_arquivo": ler_arquivo, "lembrar": lembrar}
DESCRICOES = [
    {"type": "function", "function": {"name": "ler_arquivo", "description": "Lê um arquivo da pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}}, "required": ["nome"]}}},
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
            except Exception as erro:
                saida = f"recusado: {erro}"
            mostrar(f"[ferramenta] {nome} {json.dumps(args, ensure_ascii=False)} -> {saida[:80]}")
            mensagens.append({"role": "tool", "content": saida})
    return "Parei: cheguei ao limite de rodadas.", MAX_RODADAS


if __name__ == "__main__":
    os.makedirs(PASTA, exist_ok=True)
    resposta, rodadas = responder(" ".join(sys.argv[1:]))
    print(f"{resposta}\n({rodadas} rodada(s))")
