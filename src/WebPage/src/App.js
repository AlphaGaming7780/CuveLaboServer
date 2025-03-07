// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { Graph } from './Graph/Graph.tsx';
import { UpdatedValueContextProvider } from './API/UpdatedValue.tsx';

function App() {

  return (
    <div className="App">
      	<UpdatedValueContextProvider>
			<div style={{width:"50rem", height:"25rem"}}>
				<Cuve />
			</div>
			<Graph/>
      	</UpdatedValueContextProvider>
    </div>
  );
}

export default App;
