import { useState, useEffect } from 'react';

/**
 * Custom Hook: useSensorData
 * 
 * Fetches all avaliable sensors in the database
 * 
 * @returns {Object} - An object containing:
 * - `sensorData` (Array): The array of sensors retrieved from the API.
 * - `refreshData` (Function): A function to manually refetch sensors.
 */
export const useSensorData = () => {
    const [sensorData, setSensorData] = useState([]);

    const fetchData = () => {
        fetch(`http://localhost:5000/api_v1/sensors`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                setSensorData(data);
            })
            .catch(error => console.error("Error fetching data:", error));
    };

    useEffect(() => {
        fetchData(); // Fetch data on mount
    }, []);

    return { sensorData, refreshData: fetchData };
};

/**
 * Custom Hook: useSensorEvents
 * 
 * Fetches all events associated with given sensor
 * 
 * @param {string | Number} sensorId - The ID of the sensor for which events need to be fetched.
 * 
 * @returns {Object} - An object containing:
 * - `sensorEvents` (Array): Returns all events associated with the param sensor.
 * - `refreshData` (Function): A function to manually refetch events of the sensor
 */
export const useSensorEvents = (sensorId) => {
    const [sensorEvents, setSensorEvents] = useState([]);

    const fetchData = () => {
        // env value isn't actually set, to fetch api, see useSensorData()
        fetch(`http://localhost:5000/api_v1/sensors/${sensorId}/events`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                setSensorEvents(data);
            })
            .catch(error => console.error("Error fetching data:", error));
    };

    useEffect(() => {
        fetchData();
    }, [sensorId]);

    return { sensorEvents, refreshData: fetchData };
};

/**
 * Custom Hook: useEventDetails
 * 
 * Fetches all event details associated with given event
 * 
 * @param {string | Number} sensorId - The ID of the sensor associated with this event.
 * @param {string | Number} eventId - The ID of the event for which details need to be fetched.
 * @param {boolean} hidden - if true, the duplicated packets are not displayed
 * 
 * @returns {Object} - An object containing:
 * - `eventDetails` (Array): Returns all event details (including heartbeat record, data packets, and event summary)
 * - `refreshData` (Function): A function to manually refetch events of the sensor
 */
export const useEventDetails = (sensorId, eventId, hidden) => {
    const [eventDetails, setEventDetails] = useState([]);

    const fetchData = () => {
        // env value isn't actually set, to fetch api, see useSensorData()
        const url = `http://localhost:5000/api_v1/sensors/${sensorId}/events/${eventId}`;
        const fullUrl = (hidden.hidden === true ? `${url}/hidden` : url);

        fetch(fullUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                setEventDetails(data);
            })
            .catch(error => console.error("Error fetching data:", error));
    };

    useEffect(() => {
        if (hidden != undefined){
            fetchData();
        }
    }, [sensorId, eventId, hidden]);

    return { eventDetails, refreshData: fetchData };
};

/**
 * Custom Hook: useEventDetailsDownload
 * 
 * Fetches downloadable event details for given event
 * 
 * @param {string | Number} sensorId - The ID of the sensor associated with this event.
 * @param {string | Number} eventId - The ID of the event for which downloadable need to be fetched.
 * @param {boolean} hidden - if true, the duplicated packets are not displayed
 * 
 * @returns {Object} - An object containing:
 * - `eventDetails` (Array): Returns downloadable event details
 * - `refreshData` (Function): A function to manually refetch events of the sensor
 */
export const useEventDetailsDownload = (sensorId, eventId, hidden) => {
    const [eventDetails, setEventDetails] = useState(null);

    const fetchData = async () => {
        try {
            // Fetch the CSV file from the API
            const url = `http://localhost:5000/api_v1/sensors/${sensorId}/events/${eventId}/download`;
            const fullUrl = (hidden.hidden === true ? `${url}/hidden` : url);
            const response = await fetch(fullUrl);

            // Check if the response is ok
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            // Get the response as a Blob (CSV data)
            const csvBlob = await response.blob();

            // Return the Blob to be used for download
            setEventDetails(csvBlob);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, [sensorId, eventId, hidden]);

    return { eventDetails, refreshData: fetchData };
};