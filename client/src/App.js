import './App.css';

import React, { useEffect, useState } from 'react';
import LastPrediction from './components/LatestPrediction';
import PredictForm from './components/MakePrediction';


function App(){

  


  return (
    <div>
      <div>
        <LastPrediction/>
<p>gaga</p>
      </div>

      <div>
        <PredictForm/>
      </div>
    </div>
    
  );

}

export default App;
