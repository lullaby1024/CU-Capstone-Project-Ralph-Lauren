# Bokeh App for Events Visualization

## Interface
The current version supplies four tab views for self-service event exploration. 
1. <b>Tab 1: Event Data Table</b>
    - Displays the events data in a dynamic table.
    - Features
        - Flexible filters
        - Sortable table columns
        - Text boxes for revealing long cell values
2. <b>Tab 2: Event Map</b>
    - Maps events with respect to the store
    - Features
        - Ranks of events captured by size of the circles
        - Sample top venues by rank
        - Flexible filters
        - Hover tool for revealing data
        - Zoom-in/out tools
3. <b>Tab 3: Event Count</b>
    - Summarizes events in terms of
        - Counts of events by category and rank over time
        - Counts of events by category over time
    - Features
        - Flexible filters
        - Hover tool for revealing data
        - Zoom-in/out tools
4. <b>Tab 4: Event Word Cloud</b>
    - Shows the word cloud for event labels
    - Features
        - Zoom-in/out tools
        - Word clouds generated at backend

## Installation
- Clone and switch into the directory.
- Make sure the dependencies are fulfilled by running `pip install -r requirements.txt`.

## Usage
- Run `bokeh serve --show bokeh_app --args STORE`, where `STORE` is the store name.
    - The current version supports: `ORLANDO_FOA`, `LAS_VEGAS_SOUTH`, `LAS_VEGAS_NORTH` and `LANCASTER_FSC`.
    - If not specified, a warning message will show as `'Store name should be specified using "--args STORE".'` and `STORE` 
    will be defaulted to `ORLANDO_FOA`.
- User input
    - Events data should be provided in the `data` directory using the format `events_STORE.csv`.
    - Modifications of constants in `main.py` may be required for scaling up to other locations.

## Demo
<img src="https://github.com/lullaby1024/CU_Capstone_Project_Ralph_Lauren/blob/master/bokeh_app/demo/bokeh_tab1.png" width="70%">

<img src="https://github.com/lullaby1024/CU_Capstone_Project_Ralph_Lauren/blob/master/bokeh_app/demo/bokeh_tab2.png" width="70%">

<img src="https://github.com/lullaby1024/CU_Capstone_Project_Ralph_Lauren/blob/master/bokeh_app/demo/bokeh_tab3.png" width="70%">

<img src="https://github.com/lullaby1024/CU_Capstone_Project_Ralph_Lauren/blob/master/bokeh_app/demo/bokeh_tab4.png" width="70%">

## Author
- Qi Feng
