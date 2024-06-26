"""
This file contains utilities for ipyleaflet.Map widget in Flights tab of application.
"""

from ipyleaflet import Map, Marker, LayerGroup, WidgetControl, CircleMarker, Polyline, TileLayer, AwesomeIcon, AntPath

from ipywidgets import HTML

from utils import FLIGHTS, AIRLINE_COLORS, CODES, summarize_routes_from_origin, get_coords




def clear_map(map: Map) -> None:
    """
    Clears ipyleaflet.Map from all non-TileLayer layers and all controls.
    """
    # list of all operations (removal of layers and controls)
    operations = [
        ('layer', layer) for layer in map.layers if not isinstance(layer, TileLayer)
    ] + [
        ('control', control) for control in map.controls
    ]

    # execute the removal operations
    for op_type, item in operations:
        if op_type == 'layer':
            map.remove_layer(item)
        elif op_type == 'control':
            map.remove_control(item)


def get_marker_description(code: str, city: str) -> HTML:
    mess = HTML()
    mess.value = f"""<center> Airport <i> <b>{code} </b> </i> <br> in <br> <b> <i> {city} </i> </b> <br> </center> """
    
    return mess

def get_route_description(origin, origin_city, dest, dest_city, distance, elapsed_time):
    mess = HTML()
    mess.value = f"""
        <div>
            <center> Route: </center> <br>
            <b>{origin} ({origin_city})</b> <br>

        </div>
        <div style="text-align: center; font-size: 24px; margin: 10px 0;">
            &rarr;
        </div>
            <b> {dest} ({dest_city} </b>)
        </div>
        <div>
            <i> Distance: {distance} (miles) </i> <br>
            <i> Elapsed Time Arrival: {elapsed_time} (minutes) </i>
            
        """
    

    return mess




def draw_routes(map: Map, selected_origin: str) -> None:
    routes_summary = summarize_routes_from_origin(FLIGHTS, selected_origin) # get routes from selected origin and statistics
    
    # draw airlines legend
    airlines = routes_summary['AIRLINE'].tolist()
    airline_colors = {airline: AIRLINE_COLORS[airline] for airline in set(airlines)}

    legend = create_airline_legend(airline_colors)
    widget = WidgetControl(widget = legend, position = 'topright')
    map.add(widget)
    
    # create ORIGIN marker
    origin_coords = get_coords(CODES, selected_origin)
    origin_city = routes_summary['ORIGIN_CITY'][0]


    origin_marker = CircleMarker(location = tuple(origin_coords.values()), title = selected_origin, draggable = False, color = 'green')
    
    origin_marker.popup = get_marker_description(code = selected_origin, city = origin_city)
    

    # create DEST markers and ORIGIN -> DEST lines
    
    # LayerGroups() increase efficency a lot
    markers_layer = LayerGroup()
    lines_layer = LayerGroup()

    airport_icon = AwesomeIcon(name = 'plane') # Airport icon that will be drawn on marker 

    for id, row in routes_summary.iterrows():
        dest = row['DEST'] # DEST airport shortcuts
        dest_city = row['DEST_CITY']
        airline = row['AIRLINE']

        distance = row['mean_distance']
        elapsed_time = row['mean_elapsed_time']

        try:
            dest_coords = get_coords(CODES, dest) # calculate DEST airport coords
        except:
            pass # skip in case there are no coords for airport
        
        # create DEST marker 
        dest_marker = Marker(location = tuple(dest_coords.values()), title = dest, draggable = False) # create DEST marker
        dest_marker.icon = airport_icon
        dest_marker.popup = get_marker_description(code = dest, city = dest_city)

        # create ORIGIN -> DEST line
        color = AIRLINE_COLORS[airline] # color of current airline

        # line = Polyline(
        #     locations = [
        #         tuple(origin_coords.values()),
        #         tuple(dest_coords.values()),
        #     ],
        #     color = color
        # )
        line = AntPath(
            locations = [
                tuple(origin_coords.values()),
                tuple(dest_coords.values()),
            ],
            color = color,
            hardware_accelerated = True,
            delay = 1200,
            weight = 4
        )

        line.popup = get_route_description(selected_origin, origin_city, dest, dest_city, distance, elapsed_time)

        # add markers and lines to layer groups
        markers_layer.add(dest_marker)
        lines_layer.add(line)
    
    # add layers to the map
    map.add(lines_layer)
    markers_layer.add(origin_marker)
    map.add(markers_layer)

    map.center = tuple(origin_coords.values()) # center the map at ORIGIN marker





def create_airline_legend(airline_colors: dict) -> HTML:
    """
    Create legend widget of airlines 
    """
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





