from flask import Flask, jsonify, abort, make_response, request
import pandas as pd

app = Flask(__name__)


def read_commodity(start_date, end_date, commodity_type):
    '''
    :param start_date: Start date or historical data fetch
    :param end_date: End date or historical data fetch
    :param commodity_type: Type of commodity: gold or silver
    :return: price data date wise, mean and variance of data
    '''
    #read the csv file in pandas dataframe
    df_commodity = pd.read_csv('historical_prices.csv', sep=",", thousands=',')
    #Convert the date in proper format
    df_commodity['Date'] = pd.to_datetime(df_commodity['Date'], format='%b %d, %Y')
    #Sub selecting the data in query string
    df_selected = df_commodity.loc[(df_commodity['Date'] >= start_date) &  \
                           (df_commodity['Date'] <= end_date) &
                            (df_commodity['Type'] == commodity_type)]
    mean = df_selected.mean()[0]
    variance = df_selected.var()[0]

    #Dict comprehension to store selected data and retured to calling function
    output_json = [
        {str(row['Date']).split()[0]: row['Price'] for index, row in df_selected.iterrows()}
        ]
    return output_json , mean, variance

#Endpoint URL
@app.route('/commodity', methods=['GET'])
def get_data():
    #Getting the values in query string
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        commodity_type = request.args.get('commodity_type')
        if start_date is None or end_date is None or commodity_type:
            abort(405)
        result, mean, variance = read_commodity(start_date, end_date, commodity_type)
    except KeyError as e:
        abort(404)
    #Check if data present
    if len(result[0])== 0 or not result[0]:
        abort(404)
    #Return json object
    return jsonify({'data': result[0], 'mean': mean, 'variance': variance})

#Error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Data Not Found'}), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'start_date, end_date and commodity_type are mandatory parameters'}), 405)

if __name__ == '__main__':
    app.run(debug=True, port=8080)