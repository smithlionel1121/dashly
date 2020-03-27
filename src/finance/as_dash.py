import pandas as pd
from pandas_datareader.data import DataReader
import colorlover as cl
import datetime as dt
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_renderer

df_symbol = pd.read_csv('tickers.csv')

colorscale = cl.scales['9']['qual']['Paired']

os.environ["IEX_API_KEY"] = "Tsk_7ca390476d60457cbf4481a1973fad78"
os.environ["IEX_SANDBOX"] = "enable"


def dispatcher(request):
    app = _create_app()
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }

    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request()
        except Exception as e:
            response = app.server.make_response(app.server.handle_exception(e))
        return response.get_data()
        

def _create_app():
    # app = dash.Dash()
    
    app = dash.Dash(url_base_pathname="/dash/", serve_locally=False)
    #app.config.suppress_callback_exceptions = True

    app.layout = html.Div([
        html.Div([
            html.H2('IEX Finance Explorer',
            style = {
                'display': 'inline',
                'float': 'left',
                'font-size': '2.65em',
                'margin-left': '7px',
                'font-weight': 'bolder',
                'font-family': 'Product Sans',
                'color': "rgba(117, 117, 117, 0.95)",
                'margin-top': '20px',
                'margin-bottom': '0'
            }),
            html.A('Home', href='/home/',
            style = {
                'color': 'red',
                'display': 'inline',
                'margin-left': '54%'
            })
        ]),
        dcc.Dropdown(
            id='stock-ticker-input',
            options=[{'label': s[0], 'value': s[1]} for s in zip(df_symbol.Company, df_symbol.Symbol)],
            value=[ 'AAPL', 'TSLA'],
            multi = True,
        ),
        html.Div(id='graphs')
        
    ], className="container")

    @app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])

    def update_graph(tickers):
        graphs = []
        for i, ticker in enumerate(tickers):
            try:
                df = DataReader(ticker, 'iex',
                dt.datetime(2017,1,1),
                dt.datetime.now())
            except Exception:
                graphs.append(html.H3(
                    'Data is not available for {}'.format(ticker),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
            # except Exception as e:
            #     graphs.append(html.H3(
            #         'Data is not available for {}'.format(e),
            #         style={'marginTop': 20, 'marginBottom': 20}
            #     ))
                continue

            candlestick = {
                'x': df.index,
                'open': df['open'],
                'high': df['high'],
                'low': df['low'],
                'close': df['close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }

            bb_bands = bbands(df.close)
            bollinger_traces = [{
                'x': df.index,
                'y': y,
                'type': 'scatter',
                'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))

        return graphs
    return app

def bbands(price, window_size=20, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, rolling_std, upper_band, lower_band


if __name__ == "__main__":
    app = _create_app()
    app.run_server()