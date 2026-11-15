#!/usr/bin/env python3
"""Agente do zero (aula 2): o harness mais simples, que leva o seu pedido ao modelo e devolve a resposta."""
import json, os, sys, urllib.request

MODELO = os.environ.get("MODELO", "llama3.2")
URL = os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"


def cerebro(mensagens):
    corpo = {"model": MODELO, "messages": mensagens, "stream": False, "think": False, "options": {"temperature": 0, "seed": 1}}
    pedido = urllib.request.Request(URL, json.dumps(corpo).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(pedido, timeout=600) as r:
        return json.loads(r.read())["message"]


if __name__ == "__main__":
    pedido = " ".join(sys.argv[1:])
    resposta = cerebro([{"role": "user", "content": pedido}])
    print(f"{resposta['content']}\n(modelo {MODELO})")
