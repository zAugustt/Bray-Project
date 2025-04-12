/**
 * SensorInfo Component
 * Renders a container that displays more details of the given sensor.
 * 
 * props:
 * - sensorInfo: all information of the sensor
 */
const SensorInfo = (props) => {
    const sensorInfo = props.props;
    if (sensorInfo === null) {
        return(
            <div>
                <h2 className='sensor-details-header'>Sensor Details</h2>
                <div className='sensor-details-container'>
                    Select a sensor to view more information.
                </div>
            </div>
        )
    }

    return(
        <div>
            <h2 className='sensor-details-header'>Sensor Details</h2>
            <div className='sensor-details-container'>
                <p><strong>ID:</strong> {sensorInfo.id}</p>
                {sensorInfo.devEUI !== "N/A" ? (<p><strong>DevEUI:</strong> {sensorInfo.devEUI}</p>) : (<p><strong>Aux Sensor</strong></p>)}
                {sensorInfo.numEvents != -1 ? (<p></p>) : (<p><strong>Number of Events:</strong> {sensorInfo.numEvents}</p>)}
            </div>
        </div>
    )
}

export default SensorInfo;