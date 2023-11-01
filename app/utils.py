import requests

def enviarREST(url, data, optional_headers=None):
    # - url: a URL para a qual a solicitação será enviada.
    # - data: os dados que serão enviados na solicitação.
    # - optional_headers: cabeçalhos opcionais que podem ser fornecidos. Se não fornecidos, assume-se um dicionário vazio.

    # Verifica se optional_headers não é None e atribua um dicionário vazio, se necessário.
    headers = optional_headers if optional_headers is not None else {}

    # Envia uma solicitação POST para a URL especificada com os dados e cabeçalhos fornecidos.
    response = requests.post(url, data=data, headers=headers)

    # Se o status da resposta não é 200 (OK).
    if response.status_code != 200:
        # Lança uma exceção com mensagem de erro.
        raise Exception(f"Problema com {url}, Status Code: {response.status_code}")

    # Retorna o conteúdo da resposta como texto.
    return response.text