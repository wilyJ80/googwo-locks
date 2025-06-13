# Requisitos

- Python 3

# Como rodar

- `python3 -m venv venv`

- `source venv/bin/activate` no Linux, `.\.venv\Scripts\activate` no Windows

- `pip install -r requirements.txt`

- `python3 ownership_server.py`

- Em outro terminal: `python3 ./app_a/app_a.py`

- Em outro terminal: `python3 ./app_b/app_b.py`

- Abrir `localhost:5000` no navegador para acessar o primeiro servidor, com arquivos espelhados para o servidor acessivel em `localhost:5001` e vice-versa

# Simulacao testes

- Crie um arquivo no formulario principal. Tente editar enquanto outro usuario edita: o app bloqueia. Ao visualizar com um usuario um arquivo em edicao por outro, as mudancas se refletem em intervalos poucos segundos ao arquivo ser salvo pelo editor. Os servidores compartilham o estado da posse dos arquivos em tempo de execucao.
