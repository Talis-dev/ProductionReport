import webbrowser
import os

# Caminho para o diretório do seu ambiente virtual
venv_path = 'venv'

# Caminho para o seu script Streamlit
streamlit_script_path = '_Home.py'


# Comando para ativar o ambiente virtual
activate_venv = f'{venv_path}\\Scripts\\activate'

# Comando para executar o Streamlit
streamlit_command = f'streamlit run {streamlit_script_path}'

# Executa o Streamlit em uma nova janela do terminal
os.system(f'start cmd /k "{activate_venv} && {streamlit_command}"')

# URL da aplicação Streamlit (geralmente é localhost com a porta 8501)
streamlit_url = 'http://localhost:8501'

# Abre a página do Streamlit no navegador padrão
webbrowser.open(streamlit_url)
