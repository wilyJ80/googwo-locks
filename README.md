# Requisitos

- Python 3

# Como rodar

- `python3 -m venv venv`

- `source venv/bin/activate` no Linux, `.\.venv\Scripts\activate` no Windows

- `pip install -r requirements.txt`

- `python3 pyro_server.py`

- Em outro terminal: `python3 flask_app.py`

- Abrir `localhost:8000` no navegador

# Simulacao testes

- Crie um arquivo no formulario principal. Tente editar enquanto outro usuario edita: o app bloqueia. Ao visualizar com um usuario um arquivo em edicao por outro, as mudancas se refletem em intervalos poucos segundos ao arquivo ser salvo pelo editor.
