from shiny.express import ui, input, render, output, expressify, session
from shinywidgets import render_widget, render_plotly, render_altair
from shiny import reactive


from utils import *
from map_utils import *


## Altair and dependencies
import altair as alt
import anywidget
import jsonschema
import toolz



ui.page_opts(title = "U.S Flights", fillable = True)

@reactive.calc
def origin_dest_summary():
    """
    Dynamic statistics calculation for ORIGIN -> DEST route.
    """
    summaries = summarize_from_origin(FLIGHTS, input.origin().split(',')[0])
    return summaries


@reactive.calc
def numerical_data():
    """
    Return numerical data of FLIGHTS_SAMPLE dataset.
    """
    numerical_columns = FLIGHTS_SAMPLE.select_dtypes(include=['number'])
    numerical_columns = numerical_columns.drop(['CANCELLED', 'DIVERTED', 'DOT_CODE', 'FL_NUMBER'], axis = 1)

    return numerical_columns

@reactive.calc
def flights_data():
    """
    Return FLIGHTS_SAMPLE dataset
    """
    return FLIGHTS_SAMPLE



# Application


######################################(FLIGHTS TAB)######################################
with ui.nav_panel('Flights'): 
    with ui.layout_sidebar():



        #################################(FLIGHTS.SIDEBAR)
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
                



        #################################(FLIGHTS.MAP WIDGET)
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



######################################(Data TAB)######################################
with ui.nav_panel('Data'):
    with ui.navset_pill():
        #################################(Data.RAW_DATA)
        with ui.nav_panel('Raw data'): 
            with ui.card():
                @render.data_frame
                def raw_data():
                    return FLIGHTS_SAMPLE
                



        #################################(Data.STATISTICS)
        with ui.nav_panel('Statistics'):
            with ui.card():
                with ui.accordion():

                    #################################(Data.STATICSTICS.CORRELATIONS)
                    with ui.accordion_panel('Correlations'):
                        @render_widget
                        def corr_mat():
                            numerical_columns = numerical_data()  # Assuming numerical_data() returns your dataset
                            correlation_matrix = numerical_columns.corr().round(3)
                            
                            # Flatten the correlation matrix for Altair heatmap
                            corr_flat = pd.DataFrame(correlation_matrix.stack(), columns=['correlation']).reset_index()
                            corr_flat.columns = ['variable1', 'variable2', 'correlation']
                            
                            # Create Altair heatmap
                            heatmap = alt.Chart(corr_flat).mark_rect().encode(
                                x='variable1:N',
                                y='variable2:N',
                                color='correlation:Q',
                                tooltip=['variable1', 'variable2', alt.Tooltip('correlation', format='.3f')]
                            ).properties(
                                        width = 300, 
                                        height = 300)

                            return heatmap

                    #################################(Data.STATICSTICS.DESCRIPTIVE_STATISTICS)
                    with ui.accordion_panel('Descriptive statistics'):
                        @render.data_frame
                        def descriptive_stats():
                            numerical_columns = numerical_data()
                            summary_stats = numerical_columns.describe()
                            stat_names = summary_stats.index

                            summary_stats['Statistic'] = stat_names

                            summary_stats = summary_stats[['Statistic'] + summary_stats.columns[:-1].tolist()]
                        
                            return summary_stats                   

        #################################(Data.INTARRACTIONS)     
        with ui.nav_panel('Interractions'):
            with ui.layout_columns():

                ui.input_select(id = 'var1', label = 'Variable 1', choices = NUMERIC_COLS)
                ui.input_select(id = 'var2', label = 'Variable 2', choices = NUMERIC_COLS)
            
            with ui.card():
                @render_altair
                def xy_plot():
                    numericals = numerical_data()
                    chart = alt.Chart(numericals).mark_point().encode(
                        x=input.var1(),
                        y=input.var2(),
                        tooltip=[input.var1(), input.var2()]  # Define tooltips for variables var1 and var2
                    ).interactive()  # Enable interactivity (zoom, pan, etc.)

                    return chart






        #################################(Data.DISTRIBUTIONS)   
        with ui.nav_panel('Distributions'):
            with ui.layout_columns():
                with ui.card():
                    ui.input_select('distribution_var', 'Select variable', choices=list(FLIGHTS.columns))
                with ui.card():
                    ui.input_select('distribution_color', 'Color by', choices=['None', 'AIRLINE', 'ORIGIN_CITY', 'DEST_CITY'])

            with ui.card():
                @render_altair
                def histogram_or_barplot():
                    var = input.distribution_var()
                    color = input.distribution_color()
                    data = flights_data()  # Assuming flights_data() returns your dataset
                    
                    if color != 'None':
                        if color != var:
                            data = data[[var, color]]
                            if is_numeric_dtype(data[var]):
                                chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
                                    x=alt.X(var, bin=alt.Bin(maxbins=30)),
                                    y='count()',
                                    color=alt.Color(color, legend=alt.Legend(title=color)),
                                    tooltip=[var, alt.Tooltip('count()', title='Count')]
                                )
                            else:
                                chart = alt.Chart(data).mark_bar().encode(
                                    x=var,
                                    y='count()',
                                    color=alt.Color(color, legend=alt.Legend(title=color)),
                                    tooltip=[var, alt.Tooltip('count()', title='Count')]
                                )
                        else:
                            data = data[[var]]
                            if is_numeric_dtype(data[var]):
                                chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
                                    x=alt.X(var, bin=alt.Bin(maxbins=30)),
                                    y='count()',
                                    color=alt.Color(var, legend=alt.Legend(title=var)),
                                    tooltip=[var, alt.Tooltip('count()', title='Count')]
                                )
                            else:
                                chart = alt.Chart(data).mark_bar().encode(
                                    x=var,
                                    y='count()',
                                    color=alt.Color(var, legend=alt.Legend(title=var)),
                                    tooltip=[var, alt.Tooltip('count()', title='Count')]
                                )
                    else:
                        data = data[[var]]
                        if is_numeric_dtype(data[var]):
                            chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
                                x=alt.X(var, bin=alt.Bin(maxbins=30)),
                                y='count()',
                                tooltip=[var, alt.Tooltip('count()', title='Count')]
                            )
                        else:
                            chart = alt.Chart(data).mark_bar().encode(
                                x=var,
                                y='count()',
                                tooltip=[var, alt.Tooltip('count()', title='Count')]
                            )
                    
                    # Add interactive selection
                    selection = alt.selection_multi(fields=[color], bind='legend')
                    filtered_chart = chart.add_selection(selection).transform_filter(selection)
                    
                    return filtered_chart

                        


ui.nav_spacer()


######################################(DATA DESCRIPTION TAB)######################################
with ui.nav_panel('Data description'):
    ui.markdown(f'Dataset used for this aplication is a sample of [Flight Delay and Cancellation Dataset (2019-2023)]({DATASET_SOURCE}). On the table below you can find description of individual columns:')
    with ui.card():
        ui.markdown(DESCRIPTION_HTML)



######################################(LIGHT/DARK MODE SWITCH)######################################
with ui.nav_control():
    ui.input_dark_mode(id = 'mode', mode = 'light')

            