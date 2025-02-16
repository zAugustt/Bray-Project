import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { ModuleRegistry } from '@ag-grid-community/core';
import { AgGridReact } from '@ag-grid-community/react';
// Import grid and core CSS
import '@ag-grid-community/styles/ag-grid.css';
import '@ag-grid-community/styles/ag-theme-quartz.css';
import '../../styles/sensor.css'
import ViewEventDetailsButton from './ViewEventDetailsButton';
import BackButton from '../BackButton';
import RefreshButton from '../RefreshButton';
import { useSensorEvents } from '../../apiServices';
import React, { useState, useMemo, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';

ModuleRegistry.registerModules([ClientSideRowModelModule]);

/**
 * EventTable Component
 * Renders the table that holds all events associated with the sensor selected (useParams)
 */
const EventTable = () => {
    const gridRef = useRef();
    const { sensorId } = useParams();
    const { sensorEvents, refreshData} = useSensorEvents(sensorId);
    const [rowData, setRowData] = useState([]);

    useEffect(() => {
        if (sensorEvents){
            setRowData(sensorEvents.event_datas);
        }
    }, [sensorEvents]);

    const [colDefs] = useState([
        { headerName: 'ID', field: 'id', flex: 1 },
        { headerName: 'Timestamp', field: 'timestamp', flex: 3 },
        { headerName: 'Event Details', cellRenderer: ViewEventDetailsButton, flex: 2 }
    ]);

    const defaultColDef = {
        flex: 1,
        resizable: false,
    };

    const rowSelection = useMemo(() => { 
        return {
            mode: 'singleRow',
            checkboxes: false,
            enableClickSelection: true,
        };
    }, []);

    useEffect(() => {
        if (sensorEvents && sensorEvents.event_datas) {
            const sortedData = [...sensorEvents.event_datas].sort((a, b) => b.id - a.id);
            setRowData(sortedData);
        }
    }, [sensorEvents]);

    // Return the grid component
    return (
        <div className='event-container'>
            <div className='event-back-btn-container'>
                <BackButton target='sensors' />
                <h3>Historical Data for Sensor {sensorId}</h3>
                <RefreshButton onRefresh={refreshData} />
            </div>
            <div className='column-container'>
                <div className='column'>
                    <div className='ag-theme-quartz ag-theme-bray event-table'>
                        <AgGridReact
                            ref={gridRef}
                            rowData={rowData}
                            columnDefs={colDefs}
                            defaultColDef={defaultColDef}
                            rowSelection={rowSelection}
                            suppressCellFocus={true}
                            suppressMovableColumns={true}
                            frameworkComponents={{
                                ViewEventDetailsButton: ViewEventDetailsButton, // Register the custom renderer
                            }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EventTable;
