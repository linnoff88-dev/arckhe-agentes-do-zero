# Sistema de agentes do zero

[![Sistema de agentes do zero](assets/img/capa.jpg)](https://inematds.github.io/agentes-do-zero-v72/)

**Curso grÃ¡tis (7 aulas):** https://inematds.github.io/agentes-do-zero-v72/

VocÃª monta um agente de IA peÃ§a por peÃ§a, seguindo 10 passos (objetivo, harness, modelo, ferramentas, instruÃ§Ãµes,
memÃ³ria, limites, testes, mediÃ§Ã£o e iteraÃ§Ã£o). Python puro, nenhuma biblioteca para instalar e IA grÃ¡tis no seu
computador (Ollama + `llama3.2`). No fim, o agente lÃª e grava arquivos numa pasta sÃ³, lembra de vocÃª, pede o seu OK e
se mede sozinho.

## O kit (`kit/`)

| Arquivo | O que Ã© |
|---|---|
| `aula2/agente.py` | 19 linhas: leva o pedido ao modelo e imprime a resposta |
| `aula3/agente.py` | 52 linhas: + ferramenta `ler_arquivo` e o loop (atÃ© 5 rodadas) |
| `aula4/agente.py` | 67 linhas: + instruÃ§Ãµes em `instrucoes.md` e memÃ³ria em `memoria.json` |
| `aula5/agente.py` (= `agente.py`) | 87 linhas: + pasta Ãºnica, OK antes de substituir, ferramenta `escrever_arquivo` |
| `medir.py` | 6 tarefas fixas, cada uma numa pasta limpa: acerto, tempo, rodadas e "caiu" Ã  parte |
| `instrucoes.md`, `objetivo.md` | modelos que o aluno copia e edita |
| `blocos/*.sh`, `saidas/*.txt` | os comandos de cada aula e a saÃ­da real capturada (14/11/2026) |

## O processo, do inÃ­cio ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Preparar o computador (Windows: WSL + Ubuntu) | `python3 --version` Â· ollama.com Â· `ollama pull llama3.2` | vocÃª |
| 2 | Baixar o kit | `cd ~ && git clone https://github.com/inematds/agentes-do-zero-v72` | vocÃª |
| 3 | Seguir as aulas 2 a 5 | em `~/agente-do-zero`: `cp ~/agentes-do-zero-v72/kit/aulaN/agente.py .` e `python3 agente.py "pedido"` | vocÃª |
| 4 | Medir | `cp ~/agentes-do-zero-v72/kit/medir.py . && python3 medir.py` | âš™ï¸ script |
| 5 | Iterar | `git commit` â†’ mudar uma coisa â†’ `python3 medir.py` â†’ manter ou `git restore` | vocÃª |
| 6 | Ir alÃ©m | [INTELECTO v2](https://inematds.github.io/intelecto-v2/guia/) e `python3 -m intelecto avaliar` | vocÃª |
| 7 | (ManutenÃ§Ã£o do curso) editar `conteudo/pt/aulas/*.json` com marcadores `@@bloco/@@arquivo/@@saida`, capturar e gerar | `bash kit/capturar.sh` (cada bloco pega a prÃ³pria vaga gpu; nunca embrulhar o lote) â†’ `resolver-kit.py .` â†’ `python3 gerar.py && python3 validar.py --links` | ðŸ§  sessÃ£o |

## Mais no INEMA.CLUB

- [Ficha completa deste curso](https://www.inema.club/cursos/392-sistema-de-agentes-do-zero-monte-o-seu-agente-de-ia-nos-10-passos-com-ia-gratis-no-computador/)
- [Guia: como aprender inteligÃªncia artificial](https://www.inema.club/aprender-inteligencia-artificial/)
- [Todos os cursos](https://www.inema.club/cursos/)

Formato INEMA Learning v7.2 Â· conteÃºdo aberto e gratuito Â· [inema.club](https://inema.club)

---

Projeto adaptado da comunidade INEMA TDS - Marca Arckhe