// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { WaterLevelContextProvider } from './API/WaterLevel.tsx';
import { Graph } from './Graph/Graph.tsx';
import { MotorSpeedContextProvider } from './API/MotorSpeed.tsx';

function App() {

  return (
    <div className="App">
      	<WaterLevelContextProvider>
			<MotorSpeedContextProvider>
				<div style={{width:"50rem", height:"25rem"}}>
					<Cuve />
				</div>
				<Graph/>	
			</MotorSpeedContextProvider>
      	</WaterLevelContextProvider>
    </div>
  );
}

export default App;
