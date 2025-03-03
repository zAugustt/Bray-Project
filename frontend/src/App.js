import React from 'react';
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";

import SensorPage from './pages/SensorPage';       
import EventPage from './pages/EventPage';       
import EventDetailsPage from './pages/EventDetailsPage';       

function App() {
  return (
    <Router>
        <Routes>
            {/* Home page is the list of sensors */}
            <Route exact path="/" element={<SensorPage />} />
            <Route path="/sensors" element={<SensorPage />} />
            <Route path="/events/:sensorId" element={<EventPage />} />
            <Route path="/events/:sensorId/event-details/:eventId" element={<EventDetailsPage />} />
        </Routes>
    </Router>
  );
}
export default App;