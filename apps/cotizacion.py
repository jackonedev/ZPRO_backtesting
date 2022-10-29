import pandas as pd


def criterio_valor_apertura(cotizacion, symbol):
    cotizacion.loc[:, symbol] = cotizacion["1. open"]
    cotizacion = cotizacion[symbol].to_frame()
    return cotizacion


def preparar_cotizacion(data, cotizacion):
    data = data.sort_index(ascending=True)
    cotizacion = cotizacion.sort_index(ascending=True)

    cotizacion_slice = cotizacion[data.index.min() : data.index.max()].index
    ## (!) Acá debería haber un context manager: no estoy seguro que en otro evento 7 días de offset vayan a coincidir con dataset de otra temporalidad
    if cotizacion_slice[-1] < data.index.max():
        return cotizacion[
            data.index.min() : data.index.max() + pd.offsets.DateOffset(days=7)
        ]

    result = criterio_valor_apertura(cotizacion[data.index.min() : data.index.max()])
    return result


def agregar_cotizacion(data, cotizacion):
    for i in range(len(cotizacion)):
        if i == 0:
            data.loc[: cotizacion.index[i], "Cotizacion_USD"] = cotizacion.iloc[
                i
            ].values[0]
            continue

        data.loc[
            cotizacion.index[i - 1] : cotizacion.index[i], "Cotizacion_USD"
        ] = cotizacion.iloc[i].values[0]

    return data
