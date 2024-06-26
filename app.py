from shiny.express import ui, input, render, output, expressify, session
from shinywidgets import render_widget  
from shiny import reactive


from utils import *
from map_utils import *


ui.page_opts(title = "U.S Airports", fillable = True)

@reactive.calc
def origin_dest_summary():
    """
    Dynamic statistics calculation for ORIGIN -> DEST route.
    """
    summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])
    return summaries


@reactive.calc
def numerical_data():
    numerical_columns = FLIGHTS.select_dtypes(include=['number'])
    numerical_columns = numerical_columns.drop(['CANCELLED', 'DIVERTED', 'DOT_CODE', 'FL_NUMBER'], axis = 1)

    return numerical_columns






with ui.nav_panel('Flights'): 
    with ui.layout_sidebar():
        ############################# sidebar
        with ui.sidebar(width = 600):
            ui.input_select('origin', 'Origin', choices=ORIGIN_AIRPORTS)
            with ui.accordion():
                ########################################### ORIGIN -> DEST STATISTICS                
                with ui.accordion_panel('Stats'):
                    with ui.navset_pill(id = 'statistics'): 
                        with ui.nav_panel('Airlines'): # Airport info
                            ui.markdown('*Info about airlines for route.*')
                            @render.data_frame
                            def airports_summary():
                                summaries = origin_dest_summary()
                                return summaries['airports']
                        with ui.nav_panel('DEP/ARR'):
                            ui.markdown('Info about departure/arrival times (minutes).')
                            @render.data_frame
                            def times_summary():
                                summaries = origin_dest_summary()
                                return summaries['times']
                            
                        with ui.nav_panel('In flight'):
                            ui.markdown('*Info about in flight times.*')

                            @render.data_frame
                            def inflights_summary():
                                summaries = origin_dest_summary()
                                return summaries['in_flight_times']

                        with ui.nav_panel('Duration and Distance'):
                            ui.markdown('*Info about durations and distances.*')

                            @render.data_frame
                            def duration_distance_summary():
                                summaries = origin_dest_summary()

                                return summaries['duration_distance']

                        with ui.nav_panel('Status'):
                            ui.markdown('*Sum of cancelled or diverted flights.*')

                            @render.data_frame
                            def flight_status_summary():
                                summaries = origin_dest_summary()

                                return summaries['flight_status']
                

        ########################################### Map widget

        with ui.card():
            @render_widget
            def map():
                m = Map(scroll_wheel_zoom = True, zoom = 3)
                
                return m
            @reactive.effect
            def update_map():
                clear_map(map.widget)
                selected_origin = input.origin().split(',')[0]
                draw_routes(map.widget, selected_origin)




# Data panel
with ui.nav_panel('Data'):
    with ui.navset_pill():
        with ui.nav_panel('Raw data'):
            with ui.card():
                @render.data_frame
                def raw_data():
                    return FLIGHTS_SAMPLE
        with ui.nav_panel('Statistics'):
            with ui.card():
                with ui.accordion():
                    with ui.accordion_panel('Correlations'):
                        @render_widget
                        def corr_mat():
                            numerical_columns = numerical_data()
                            correlation_matrix = numerical_columns.corr().round(3)

                            return px.imshow(correlation_matrix, text_auto= True)

                    with ui.accordion_panel('Descriptive statistics'):
                        @render.data_frame
                        def descriptive_stats():
                            numerical_columns = numerical_data()
                            summary_stats = numerical_columns.describe()
                            stat_names = summary_stats.index

                            summary_stats['Statistic'] = stat_names

                            summary_stats = summary_stats[['Statistic'] + summary_stats.columns[:-1].tolist()]
                        
                            return summary_stats                   

                                
        with ui.nav_panel('Interractions'):
            with ui.layout_columns():
                ui.input_select(id = 'var1', label = 'Variable 1', choices = NUMERIC_COLS)
                ui.input_select(id = 'var2', label = 'Variable 2', choices = NUMERIC_COLS)
            
            with ui.card():
                @render_widget
                def xy_plot():
                    numericals = numerical_data()
                    plot = px.scatter(data_frame = numericals, x = input.var1(), y = input.var2())

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
                        if color != var: # case color != var
                            data = FLIGHTS_SAMPLE[[var, color]]
                            if is_numeric_dtype(data[var]):
                                return px.histogram(data_frame=data, x = var, color = color, hover_name = var, opacity = 0.7)
                            else:
                                return px.bar(data_frame = data, x =
                                var, color = color, hover_name = var)
                            
                        data = FLIGHTS_SAMPLE[[var]] # case color == var
                        if is_numeric_dtype(data[var]):
                            return px.histogram(data_frame=data, x = var, color = var, hover_name = var, opacity = 0.7)
                        else:
                            return px.bar(data_frame = data, x =
                            var, color = var, hover_name = var)
      
ui.nav_spacer()
with ui.nav_panel('Data description'):
    ui.markdown(f'Dataset used for this aplication is a sample of [Flight Delay and Cancellation Dataset (2019-2023)]({DATASET_SOURCE}). On the table below you can find description of individual columns:')
    with ui.card():
        ui.markdown(DESCRIPTION_HTML)




with ui.nav_control():
    ui.input_dark_mode(id = 'mode', mode = 'light')

            