import requests

def call_azure_function():
    url = 'https://func-poc-timeout-test.azurewebsites.net/api/http_trigger'  # Azure FunctionのエンドポイントURL
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f'Response: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Error calling Azure Function: {e}')

if __name__ == '__main__':
    call_azure_function()
