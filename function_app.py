import azure.functions as func
import logging
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTPトリガー関数がリクエストを処理しました。')

    try:
        # クエリパラメータからsleeptimeを取得
        sleep_time = req.params.get('sleeptime')
        if not sleep_time:
            try:
                req_body = req.get_json()
                sleep_time = req_body.get('sleeptime')
            except ValueError:
                sleep_time = None

        if sleep_time:
            try:
                sleep_time = int(sleep_time)
                if sleep_time <= 0:
                    raise ValueError
            except ValueError:
                return func.HttpResponse('無効なスリープ時間が指定されました。正の整数を入力してください。', status_code=400)
        else:
            return func.HttpResponse('スリープ時間が指定されていません。', status_code=400)

        logging.info(f'スリープ時間: {sleep_time} 秒')

        def generate():
            start_time = time.time()
            elapsed_time = 0

            while elapsed_time < sleep_time:
                time.sleep(10)
                elapsed_time = time.time() - start_time
                message = f'経過時間: {int(elapsed_time)} 秒\n'
                yield message
                logging.info(message.strip())

            yield f'合計スリープ時間: {sleep_time} 秒\n'

        return func.HttpResponse(generate(), status_code=200, mimetype='text/plain')

    except Exception as e:
        logging.error('サーバーでエラーが発生しました: {}'.format(str(e)))
        return func.HttpResponse('サーバーでエラーが発生しました。', status_code=500)
