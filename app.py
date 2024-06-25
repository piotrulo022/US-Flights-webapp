from ipyleaflet import Map, Marker, LayerGroup, WidgetControl, CircleMarker, Popup, Polyline, TileLayer, AwesomeIcon, Icon
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



with ui.nav_panel('Flights'): 
    with ui.layout_sidebar():
        ############################# sidebar
        with ui.sidebar(width = 800):
            ui.input_select('origin', 'Origin', choices=origin_airports)
            with ui.accordion():
                with ui.accordion_panel('Stats'):
                    with ui.navset_pill(id = 'statistics'): 
                            
                        with ui.nav_panel('Airports'):
                            @render.data_frame
                            def airports_summary():
                                summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])

                                return summaries['airports']
                            
                        with ui.nav_panel('Departure and Arrival times'):
                            @render.data_frame
                            def times_summary():
                                summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])

                                return summaries['times']
                            
                        with ui.nav_panel('In-Flight times'):
                            @render.data_frame
                            def inflights_summary():
                                summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])

                                return summaries['in_flight_times']

                        with ui.nav_panel('Duration and distance'):
                            @render.data_frame
                            def duration_distance_summary():
                                summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])

                                return summaries['duration_distance']

                        with ui.nav_panel('Flight status'):
                            @render.data_frame
                            def flight_status_summary():
                                summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])

                                return summaries['flight_status']

        #############################
        ############################# map
        @render_widget
        def map():
            m = Map(scroll_wheel_zoom = True, zoom = 3)

            return m
        @reactive.effect
        def update_map():
            clear_map(map.widget)

            selected_origin = input.origin().split(',')[0]
            origin_coords = get_coords(CODES, selected_origin)


            map.widget.center = tuple(origin_coords.values())
            draw_routes(map.widget, selected_origin)
with ui.nav_panel('Data'):
    with ui.navset_pill():
        with ui.nav_panel('Raw data'):
            with ui.card():
                @render.data_frame
                def raw_data():
                    return FLIGHTS_HEAD
                    # return FLIGHTS
                    # return render.DataTable(FLIGHTS_HEAD, filters = True, selection_mode='rows')

        with ui.nav_panel('Statistics'):
            with ui.card():
                with ui.accordion():
                    with ui.accordion_panel('Correlations'):
                        @render_widget
                        def corr_mat():
                            numerical_columns = FLIGHTS.select_dtypes(include=['number'])
                            numerical_columns = numerical_columns.drop(['CANCELLED', 'DIVERTED', 'DOT_CODE', 'FL_NUMBER'], axis = 1)
                            correlation_matrix = numerical_columns.corr().round(3)

                            return px.imshow(correlation_matrix, text_auto=True)
                    with ui.accordion_panel('Descriptive statistics'):
                        @render.data_frame
                        def xd():
                            numerical_columns = FLIGHTS.select_dtypes(include=['number'])
                            numerical_columns = numerical_columns.drop(['CANCELLED', 'DIVERTED', 'DOT_CODE', 'FL_NUMBER'], axis = 1)
                            summary_stats = numerical_columns.describe()
        
                            # Additional customization if needed (optional)
                            # For example, adding column names to the summary table
                            stat_names = summary_stats.index
                            summary_stats['Statistic'] = stat_names

                            summary_stats = summary_stats[['Statistic'] + summary_stats.columns[:-1].tolist()]
                        
                            return summary_stats                            
                        

        
        with ui.nav_panel('Interractions'):
            with ui.layout_columns():
                ui.input_select(id = 'var1', label = 'Variable 1', choices = NUMERIC_COLS)
                ui.input_select(id = 'var2', label = 'Variable 2', choices = NUMERIC_COLS)
            
            # pass
            with ui.card():
                @render_widget
                def xy_plot():
                    plot = px.scatter(data_frame = FLIGHTS, x = input.var1(), y = input.var2())

                    return plot
 

        with ui.nav_panel('Distributions'):
            with ui.layout_columns():
                with ui.card():
                    ui.input_select('distribution_var', 'Select variable', choices=list(FLIGHTS.columns))
                with ui.card():
                    ui.input_select('distribution_color', 'Color by', choices=['None', 'AIRLINE', 'ORIGIN_CITY', 'DEST_CITY'])

            with ui.card():
                @render_widget
                def histogram_or_barplot():
                    var = input.distribution_var()
                    color = input.distribution_color()
                
                    if color != 'None':
                        if color != var:
                            data = FLIGHTS_SAMPLE[[var, color]]
                        else:
                            data = FLIGHTS[var]
                            
                        if is_numeric_dtype(data[var]):
                            return px.histogram(data_frame=data, x = var, color = color, hover_name = var, opacity = 0.7)
                        else:
                            return px.bar(data_frame = data, x =
                             var, color = color, hover_name = var)
                    else:
                        data = FLIGHTS_SAMPLE[[var]]

                        if is_numeric_dtype(data[var]):
                            return px.histogram(data_frame=data, x = var, hover_name = var, opacity = 0.7)
                        else:
                            return px.bar(data_frame = data, x = var, hover_name = var)
               
ui.nav_spacer()
with ui.nav_control():
    ui.input_dark_mode(id = 'mode')

            



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
    
    DEST_AIRPORT_ICON = AwesomeIcon(name = 'plane')
    
    for id, row in routes_summary.iterrows():
        try:
            dest = row['DEST']
            origin_city = row['ORIGIN_CITY']
            airline = row['AIRLINE']
            dest_city = row['DEST_CITY']
            distance = row['mean_distance']

            dest_coords = get_coords(CODES, dest)

            color = AIRLINE_COLORS[airline]

            dest_marker = Marker(location = tuple(dest_coords.values()), title = dest, draggable = False)
            dest_marker.icon = DEST_AIRPORT_ICON
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
    origin_marker = CircleMarker(location = tuple(origin_coords.values()), title = selected_origin, draggable = False, color = 'red')
    
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
