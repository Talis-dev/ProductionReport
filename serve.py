from waitress import serve
import os

def run():
    os.system("python streamlit run _Home.py")
    
if __name__ == '__main__':
    serve(run, host='192.168.0.37', port=8501)
