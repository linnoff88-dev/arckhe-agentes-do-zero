cd ~/agente-do-zero
git config --global user.name > /dev/null || git config --global user.name "Seu Nome"          # só na 1ª vez
git config --global user.email > /dev/null || git config --global user.email "voce@exemplo.com"
git init -q && git add . && git commit -qm "antes da mudança"
echo 'Se a resposta já está em "O que você sabe do dono", responda direto, sem ferramenta.' >> instrucoes.md
python3 medir.py | tail -2
git restore instrucoes.md
MODELO=llama3.1:8b python3 medir.py | tail -2     # o modelo baixado na aula 2
