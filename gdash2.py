import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import os

# Carga la plantilla de figura 'slate' para mantener la coherencia en el diseño gráfico
load_figure_template('slate')

# Inicializa la aplicación Dash con el tema de Bootstrap 'SLATE'
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Importa módulos y rutas
from glob import glob
import sensoresCallbacks  # Módulo de callbacks para sensores
ruta_imagen = os.path.join('images', 'logo2.png')
ruta_imagen2 = os.path.join('images', 'logo.png')

# Configuración del diseño de la aplicación
app.layout = html.Div(
    [
        # Intervalo para la actualización periódica de la aplicación
        dcc.Interval(
            id='intervalo-actualizacion',
            interval=10*1000,  # Intervalo en milisegundos (cada 10 segundos)
            n_intervals=0  # Valor inicial de n_intervals
        ),
       
        # Almacenamiento de datos para la sesión
        dcc.Store(id='storeJ'),

        # --------------------- Imagenes del logo -------------------------------
        html.Img(
            src=app.get_asset_url(ruta_imagen),
            alt='Imagen de ejemplo',
            style={'width': '25%', 'height': 'auto', 'backgroundColor': 'white', 'padding': '0px'}
        ),
        html.Img(
            src=app.get_asset_url(ruta_imagen2),
            alt='Imagen de ejemplo',
            style={'width': '25%', 'height': 'auto', 'backgroundColor': 'white', 'padding': '0px', 
                   'margin-right': '0'}
        ),

        # -------------------- Título principal de la aplicación --------------------
        html.H1(
            "SiCoBioNa",
            style={
                'text-align': 'center', 'font-family': 'Playfair Display, serif', 'font-weight': 'bold',
                'text-shadow': '1px 1px 0px rgba(0, 0, 200, 5)', 'color': 'white', 
                'text-decoration': 'underline'
            }
        ),
        
        # --------------------- Subtítulo de la aplicación -------------------------
        html.H1(
            "Sensores Ambientales",
            style={
                'text-align': 'center', 'font-family': 'Playfair Display, serif', 'font-weight': 'bold',
                'text-shadow': '1px 1px 0px rgba(0, 0, 200, 5)', 'color': 'white', 
                'text-decoration': 'underline'
            }
        ),

        # ------------------- Selectores de Sensores y Variables -------------------
        dcc.Store(id='data-store'),  # Almacena los datos seleccionados de sensores y variables
        dcc.Dropdown(id='dropSensor', options=[], multi=True, style={'font-weight': 'bold'}),  # Selector de sensores
        dcc.Dropdown(id='dropVar', options=[], multi=True, style={"width": 800, 'font-weight': 'bold'}),  # Selector de variables
        
        # -------------------------- Registro Histórico ----------------------------
        html.H1(
            "Registro Histórico:",
            style={
                'color': 'black', 'text-align': 'center', 'font-family': 'Playfair Display, serif',
                'text-shadow': '1px 1px 0px rgba(0, 0, 200, 5)', 'color': 'white', 
                'font-weight': 'bold', 'text-decoration': 'underline'
            }
        ),
        html.Div(id='figures-container')  # Contenedor para gráficos o figuras históricas
    ],
    style={
        'background-image': 'url("https://e1.pxfuel.com/desktop-wallpaper/817/172/desktop-wallpaper-new-sensor-detects-ever-smaller-nanoparticles-nanoparticles.jpg")',
        'background-size': 'cover',  # La imagen cubre todo el contenedor
        'background-position': 'center',  # Posiciona la imagen en el centro
        'background-repeat': 'no-repeat',  # No repite la imagen de fondo
        'height': '100vh'  # Ajusta la altura al 100% de la ventana del navegador
    }
)

# Ejecuta la aplicación en el puerto 8050, permitiendo acceso desde cualquier IP (host='0.0.0.0')
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)

# La aplicación estará disponible en http://127.0.0.1:8050/
