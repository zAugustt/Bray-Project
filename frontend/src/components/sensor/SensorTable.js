import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { ModuleRegistry } from '@ag-grid-community/core';
import { AgGridReact } from '@ag-grid-community/react';
// Import grid and core CSS
import '@ag-grid-community/styles/ag-grid.css';
import '@ag-grid-community/styles/ag-theme-quartz.css';
import '../../styles/sensor.css'
import SensorInfo from './SensorInfo';
import ViewEventsButton from './ViewEventsButton';
import RefreshButton from '../RefreshButton';
import { useSensorData } from '../../apiServices';
import React, { useState, useMemo, useRef, useEffect } from 'react';

ModuleRegistry.registerModules([ClientSideRowModelModule]);

/**
 * SensorTable Component
 * Renders the table that display all sensors in the database
 */
const SensorTable = () => {
    const gridRef = useRef();
    const [selectedRowData, setSelectedRowData] = useState(null);

    const { sensorData, refreshData } = useSensorData();
    
    const [rowData, setRowData] = useState(sensorData);

    useEffect(() => {
        if(sensorData) {
            setRowData(sensorData);
        }
    }, [sensorData]);

    const Refresh = () => {
        refreshData();
    }

    const [colDefs] = useState([
        { headerName: 'ID', field: 'id', flex: 1 },
        { headerName: 'DevEUI', field: 'devEUI', flex: 3 },
        { headerName: 'Sensor Details', cellRenderer: ViewEventsButton, flex: 2 }
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

    const onRowSelected = (event) => {
        if (event.node.selected) {
          setSelectedRowData(event.data);
        }
    };

    // Return the grid component
    return (
        <div className='sensor-container'>
            <RefreshButton onRefresh={Refresh} />
            <div className='split-container'>
                <div className='column left-column'>
                    <div className='ag-theme-quartz ag-theme-bray sensor-table'>
                        <AgGridReact
                            ref={gridRef}
                            rowData={rowData}
                            columnDefs={colDefs}
                            defaultColDef={defaultColDef}
                            rowSelection={rowSelection}
                            onRowSelected={onRowSelected}
                            suppressCellFocus={true}
                            suppressMovableColumns={true}
                            frameworkComponents={{
                                viewEventsButton: ViewEventsButton, // Register the custom renderer
                            }}
                        />
                    </div>
                </div>
                <div className='column right-column'>
                    <SensorInfo props={selectedRowData} />
                </div>
            </div>
        </div>
    );
};

export default SensorTable;
