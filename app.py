from ipyleaflet import Map, Marker, LayerGroup, WidgetControl, CircleMarker, Popup, Polyline, TileLayer
from shiny.express import ui, input, render, output, expressify
from shinywidgets import render_widget  
from utils import *
from shiny import reactive
from ipywidgets import HTML

origin_airports = get_origins(FLIGHTS)

def clear_map(map: Map) -> None:
    layers_to_remove = [layer for layer in map.layers if not isinstance(layer, TileLayer)]
    controls_to_remove = [control for control in map.controls]
    
    for layer in layers_to_remove:
        map.remove_layer(layer)

    for control in controls_to_remove:
        map.remove_control(control)




ui.page_opts(title = "U.S airports flights dashboard", fillable = True)


with ui.navset_pill(id = 'tab'):
    with ui.nav_panel('Flights'): 
        with ui.layout_sidebar():
            ############################# sidebar
            with ui.sidebar():
                ui.input_select('origin', 'Origin', choices=origin_airports)
                with ui.accordion():
                    with ui.accordion_panel('Stats'):
                        @render.data_frame
                        def _():
                            selected_origin = input.origin()
                            routes_summary = summarize_routes_from_origin(FLIGHTS, selected_origin)

                            return routes_summary
            #############################
            ############################# map
            @render_widget
            def map():
                m = Map(scroll_wheel_zoom = True, zoom = 3)
    
                return m
            @reactive.effect
            def update_map():
                clear_map(map.widget)

                selected_origin = input.origin()
                origin_coords = get_coords(CODES, selected_origin)


                map.widget.center = tuple(origin_coords.values())
                draw_routes(map.widget, selected_origin)

                



def draw_routes(map, selected_origin):

    marker_layer = LayerGroup()
    routes_summary = summarize_routes_from_origin(FLIGHTS, selected_origin)
    airlines = routes_summary['AIRLINE'].tolist()
    airline_colors = {airline: AIRLINE_COLORS[airline] for airline in set(airlines)}
    legend = create_airline_legend(airline_colors)
    widget = WidgetControl(widget = legend, position = 'topright')
    
    map.add(widget)

    origin_coords = get_coords(CODES, selected_origin)
    map.center = tuple(origin_coords.values()) 
    
    for id, row in routes_summary.iterrows():
        try:
            dest = row['DEST']
            origin_city = row['ORIGIN_CITY']
            airline = row['AIRLINE']
            dest_city = row['DEST_CITY']
            distance = row['mean_distance']

            dest_coords = get_coords(CODES, dest)

            color = AIRLINE_COLORS[airline]

            dest_marker = CircleMarker(location = tuple(dest_coords.values()), title = dest, draggable = False)
            marker_layer.add_layer(dest_marker)         
            line = Polyline(
                locations = [
                    tuple(origin_coords.values()),
                    tuple(dest_coords.values()),
                ],
                color = color
            )

            mess = HTML()
            mess.value = f"""
                <div>
                    Route: <br>
                    <b>{selected_origin} ({origin_city})</b> <br>

                </div>
                <div style="text-align: center; font-size: 24px; margin: 10px 0;">
                    &rarr;
                </div>
                    <b> {dest} ({dest_city} </b>)
                </div>
                <div>
                    <i> Distance: {distance} (km) </i>
                """

            pop = Popup(child = mess)

            line.popup = pop
            line.on_mouseover(pop)

            map.add(line)

        except:
            # print(dest_coords)
            pass


    map.add_layer(marker_layer)
    origin_marker = Marker(location = tuple(origin_coords.values()), title = selected_origin, draggable = False, color = 'red')
    
    message1 = HTML()
    message1.value = "<b> ::::::: </b>"

    # Popup with a given location on the map:
    popup = Popup(
        location=tuple(origin_coords.values()),
        child=message1,
        close_button=False,
        auto_close=False,
        close_on_escape_key=False
    )
    # map.widget.add(popup)
    origin_marker.popup = popup
    map.add(origin_marker)

def create_airline_legend(airline_colors):
    # Start the HTML content with styles
    html_content = """
                <style>
                    .legend {
                        list-style-type: none;
                        padding: 0;
                        margin: 0;
                        font-family: Arial, sans-serif;
                    }
                    .legend li {
                        margin: 5px 0;
                        display: flex;
                        align-items: center;
                    }
                    .legend .color-box {
                        width: 20px;
                        height: 20px;
                        margin-right: 10px;
                        border: 1px solid #000;
                        flex-shrink: 0;
                        background-color: rgba(255, 0, 0, 0.5); /* Default opacity */
                    }
                </style>
                <div>
                    <h2>Airline Colors Legend</h2>
                    <ul class="legend">
                    """
    
    # Generate the list items dynamically
    for airline, color in airline_colors.items():
        html_content += f'<li><div class="color-box" style="background-color: {color};"></div>{airline}</li>'
    
    # Close the HTML content
    html_content += """
        </ul>
        </div>
    """
    
    # Adjust opacity for all color boxes
    opacity_style = "<style>.color-box { opacity: 0.8; }</style>"
    html_content = html_content.replace("</style>", f"{opacity_style}</style>")
    
    # Create the HTML widget and return it
    return HTML(value=html_content)


# def create_airline_legend(airline_colors):
#     # Start the HTML content with styles
#     html_content = """
#                 <style>
#                     .legend {
#                         list-style-type: none;
#                         padding: 0;
#                         margin: 0;
#                         font-family: Arial, sans-serif;
#                     }
#                     .legend li {
#                         margin: 5px 0;
#                         display: flex;
#                         align-items: center;
#                     }
#                     .legend .color-box {
#                         width: 20px;
#                         height: 20px;
#                         margin-right: 10px;
#                         border: 1px solid #000;
#                         flex-shrink: 0;
#                         background-color: rgba(255, 0, 0, 0.5);
#                     }
#                 </style>
#                 <div>
#                     <h2>Airline Colors Legend</h2>
#                     <ul class="legend">
#                     """
    
#     # Generate the list items dynamically
#     for airline, color in airline_colors.items():
#         html_content += f'<li><div class="color-box" style="background-color: {color};"></div>{airline}</li>'
    
#     # Close the HTML content
#     html_content += """
#         </ul>
#         </div>
#     """
    
#     # Create the HTML widget and return it
#     return HTML(value=html_content)