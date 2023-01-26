from api import app, jsonify, request
import importlib


@app.route('/', methods=['GET', 'POST'])
def get():

    try:
        networkInfo = request.get_json(force=True)

        # dynamic module import and object creation
        if(not networkInfo['networkName']):
            raise Exception("netWork name is not defined.")

        className = networkInfo['networkName']
        NetworkClass = importlib.import_module(
            f'api.networks.{className}Class'
        )
        Network = getattr(NetworkClass, className)(networkInfo)

        transactions = Network.scrapTransactions()

        if(transactions and len(transactions) > 0):
            header = zip(transactions[0].keys(), transactions[0].keys())
            return jsonify({'status': 200, 'data': transactions, 'header': dict(header)})
        else:
            raise Exception("Data not found. Please retry")

    except Exception as err:
        # err.args # to fetch all args from exception
        return jsonify({'status': 400, 'data': str(err)})


@app.route('/test', methods=['GET', 'POST'])
def test():

    import time

    try:
        args = []
        if(request.method == 'POST'):
            args = request.get_json(force=True)

        if(len(args) > 0):
            data = [
                {
                    "clickRefHash": "49-OBS-5e3db88b46bbe49pt",
                    "click_date": "2020-02-07 12:02:17",
                    "clickref": "49-OBS-5e3db88b46bbe49",
                    "commission": "3,00€".replace(',', '.').replace('€', ''),
                    "cwhen": "2020-02-07 12:02:17",
                    "dateCreated": "2020-02-12 14:13:58",
                    "details": "PL_BITCOIN-PROFIT_CPL",
                    "networkClass": "api.networks.AwinPtClass",
                    "orderDate": "2020-02-07 12:02:17",
                    "orderValue": "3,00€".replace(',', '.').replace('€', ''),
                    "reference_id": "1027c15fa261e5f5f7cfe623a9fe5f",
                    "status": 3,
                    "unique_code": ""
                },
                {
                    "clickRefHash": "89-OBS-5e3d7129173ef89pt",
                    "click_date": "2020-02-07 06:16:29",
                    "clickref": "89-OBS-5e3d7129173ef89",
                    "commission": "6,00€".replace(',', '.').replace('€', ''),
                    "cwhen": "2020-02-07 06:16:29",
                    "dateCreated": "2020-02-12 14:13:58",
                    "details": "ES_SEGUROS-SANTA-LUCIA_CPL",
                    "networkClass": "api.networks.AwinPtClass",
                    "orderDate": "2020-02-07 06:16:29",
                    "orderValue": "6,00€".replace(',', '.').replace('€', ''),
                    "reference_id": "102fe22ffffcef158d6d7c84b25cc4",
                    "status": 3,
                    "unique_code": ""
                }]
            print(data[0].keys())
            return jsonify({'data': data, 'status': dict(zip(data[0].keys(), data[0].keys()))})
        else:
            # raise Exception("testing raise exception.")
            return jsonify({'status': "else part executed"})
    except Exception as err:
        return jsonify({'status': 400, 'data': str(err)})
