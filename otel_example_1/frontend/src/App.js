import logo from './logo.svg';
import './App.css';
import RollDiceButton from './components/RollDiceButton';
import React, { useState } from 'react';
import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
    applicationId: `abcd58fb-8396-42f5-bbe0-a00bc4fc6fc4`,
    clientToken: `pub7991045935375db961055933e01d7291`,
    site: 'datadoghq.com',
    service:'otel',
    env:'justice',
    // Specify a version number to identify the deployed version of your application in Datadog 
    // version: '1.0.0', 
    sessionSampleRate:100,
    sessionReplaySampleRate: 100,
    trackUserInteractions: true,
    trackResources: true,
    trackLongTasks: true,
    defaultPrivacyLevel:'mask-user-input',
    allowedTracingUrls: [
      {
        match: `http://localhost:5500`,
        propagatorTypes: ["tracecontext"],
    },
    ],
});
    
datadogRum.startSessionReplayRecording();

function App() {
  const [responseData, setResponseData] = useState([]);

  const addData = (data) => {
    //append data to data object
    setResponseData([...responseData, data]);
  }
  const imageStyle = {
    width: '20%',     // Ensure the image fills the container horizontally
    height: '20%',    // Ensure the image fills the container vertically
    objectFit: 'contain', // Or 'cover', based on your requirement
  };


  return (
    <div className="App">
      <RollDiceButton dataHandler={(data) => addData(data)}/>
      <p>On button click, this will make a request to the backend where the Datadog tracer is instrumented.
      </p>
      <div className="data-row-title">
          <h1>Dice</h1>
          <h1>Trace Id</h1>
        </div>
      <div className="data-container">

      {
        (responseData) && responseData.map((data, index) => {
          let temp = data.dice;
          if (temp > 5) {
            return (
              <div className="data-row" key={index}>
                <p>{data.dice}</p>
                <img src={data.trace} style={imageStyle}></img>
              </div>
          )
          }
          return (
              <div className="data-row" key={index}>
                <p>{data.dice}</p>
                <p>{data.trace}</p>
              </div>
            
          )
        })
      }
      </div>
    </div>
  );
}

export default App;
