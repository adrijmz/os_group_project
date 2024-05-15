import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from rdflib import Graph

# Crear el grafo RDF
g = Graph()
# Cargar el grafo desde un archivo RDF existente o construirlo desde cero
g.parse("src/functionalities/papers.xml")

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la interfaz
app.layout = html.Div([
    html.H1("Consulta SPARQL en RDF Graph"),
    dcc.Textarea(id="query-input", placeholder="Introduce tu consulta SPARQL aquí", style={"width": "100%", "height": "200px"}),
    html.Button("Ejecutar Consulta", id="submit-button", n_clicks=0),
    html.Div(id="output")
])

# Callback para ejecutar la consulta SPARQL y mostrar los resultados
@app.callback(
    Output("output", "children"),
    [Input("submit-button", "n_clicks")],
    [Input("query-input", "value")]
)
def execute_query(n_clicks, query):
    if n_clicks > 0:
        results = g.query(query)
        result_str = "\n".join([str(row) for row in results])
        return html.Pre(result_str)
    else:
        return ""

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
