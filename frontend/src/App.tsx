import React from 'react';
import './App.css';
import CameraDisplay from "./components/CameraDisplay";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <CameraDisplay cameraSwitchUrl={'/camera_switch'} />
      </header>
    </div>
  );
}

export default App;
