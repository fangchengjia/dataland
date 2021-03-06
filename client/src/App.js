import React, { Component } from 'react';
import { withScriptjs, withGoogleMap, 
KmlLayer, GoogleMap } from "react-google-maps"
import './App.css';
import { Switch, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import ReportDetailPage from './Pages/ReportDetailPage'



// const MyMapComponent = withScriptjs(withGoogleMap((props) =>
//   <GoogleMap defaultZoom={6} 
//       defaultCenter={{ lat: -40.9006, lng: 174.8860 }}>
//     <KmlLayer
//       url="http://127.0.0.1:8000/media/nz-post-postcode-boundaries.kml"
//     />
//   </GoogleMap>
// ))


class App extends Component {
  render() {
    return (
      <div className="App">
        {/* <MyMapComponent
          googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places"
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `620px` }} />}
          mapElement={<div style={{ height: `100%` }} />}
        /> */}

        <Switch>
          <Route exact path="/" component={HomePage} />
          <Route exact path="/report/:id" component={ReportDetailPage} />
        </Switch>
      </div>
    );
  }
}

export default App;
