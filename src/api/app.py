import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from rdflib import Graph
import re

def get_variables(query):
    select_pattern = re.compile(r'SELECT\s+(.*?)\s+WHERE', re.IGNORECASE | re.DOTALL)

    # Buscar las variables en la consulta
    match = select_pattern.search(query)
    if match:
        variables_string = match.group(1)
        variables = [var.strip() for var in variables_string.split() if var.startswith('?')]
        return variables
    
    return []

# Crear el grafo RDF
g = Graph()
# Cargar el grafo desde un archivo RDF existente o construirlo desde cero
g.parse("papers.xml")

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
    result_str = ""
    if n_clicks > 0:
        results = g.query(query)

        variables_cleaned = []
        variables = get_variables(query)
        for var in variables:
            variables_cleaned.append(var[1:])

        for row in results:
            row = str(row)[1:-1]
            row_split = row.split(", ")
            for i in range(len(row_split)):
                result_str += variables_cleaned[i] + ": " + row_split[i] + "\n"
            result_str += "\n"
        
        result_str = result_str.replace("rdflib.term.Literal", "")
        
        return html.Pre(result_str)
    else:
        return ""

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
