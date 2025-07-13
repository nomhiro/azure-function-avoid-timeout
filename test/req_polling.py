import requests

def send_stream_request(sleep_time):
    url = 'https://func-poc-timeout-test.azurewebsites.net/api/http_trigger?sleeptime={}'.format(sleep_time)
    headers = {
        'Accept': 'text/event-stream'
    }
    try:
        with requests.get(url, headers=headers, stream=True, timeout=sleep_time + 60) as response:
            response.raise_for_status()  # ステータスコードが200でない場合、例外を発生させる
            for line in response.iter_lines():
                if line:
                    print(line.decode('utf-8'))
    except requests.exceptions.Timeout:
        print('リクエストがタイムアウトしました。')
    except requests.exceptions.HTTPError as errh:
        print('HTTPエラーが発生しました:', errh)
    except requests.exceptions.ConnectionError as errc:
        print('接続エラーが発生しました:', errc)
    except requests.exceptions.RequestException as err:
        print('リクエストエラーが発生しました:', err)
    except Exception as e:
        print('予期しないエラーが発生しました:', e)

if __name__ == "__main__":
    sleep_time = 300  # スリープ時間を秒で指定
    send_stream_request(sleep_time)
