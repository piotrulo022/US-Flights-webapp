from ipyleaflet import Map, Marker, LayerGroup, CircleMarker, Polyline
from shiny.express import ui, input, render, output
from shinywidgets import render_widget  
from utils import *


from ipywidgets import HTML
airports = get_origins()

ui.page_opts(title = "Siema", fillable = True)


with ui.navset_pill(id = 'tab'):
     with ui.nav_panel('Flights'): 
        @render_widget  
        def map():
            selected_origin = input.origin()
   
            routes = summarize_routes_from_origin(selected_origin)
            print(routes)
            origin_coords = get_coords(selected_origin)
            m = Map(scroll_wheel_zoom=True, zoom = 3)
            marker_layer = LayerGroup()
            origin_marker = Marker(location = tuple(origin_coords.values()), title = selected_origin, draggable = False)
            marker_layer.add_layer(origin_marker)

            for id, row in routes.iterrows():
                dest = row['dest']
                dest_coords = get_coords(dest)
                dest_marker = CircleMarker(location = tuple(dest_coords.values()), title = dest, draggable = False)
                marker_layer.add_layer(dest_marker)

                line = Polyline(
                    locations = [
                        tuple(origin_coords.values()),
                        tuple(dest_coords.values()),
                    ]
                )
                
                m.add(line)
   
            m.add_layer(marker_layer)
            return m

          
        with ui.panel_absolute(draggable=True):
            ui.input_select('origin', 'Origin', choices = airports)
            
            pass