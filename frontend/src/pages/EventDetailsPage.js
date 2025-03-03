// Modal to display details of an event
import React from "react";
import Header from '../components/Header';
import DetailsContainer from "../components/event-details/DetailsContainer";

const EventDetailsPage = () => {
    return (
        <div>
            <Header />
            <DetailsContainer />
        </div>
    );
};

export default EventDetailsPage;