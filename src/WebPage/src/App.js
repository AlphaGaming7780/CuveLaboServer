// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { Graph } from './Graph/Graph.tsx';
import { UpdatedValueContextProvider } from './API/UpdatedValue.tsx';
import { BaseDataContextProvider } from './API/GetBaseData.tsx';

function App() {



  return (
    <div className="App">
		<BaseDataContextProvider>
			<UpdatedValueContextProvider>
				<div style={{width:"50rem", height:"25rem"}}>
					<Cuve />
				</div>
				<Graph/>
			</UpdatedValueContextProvider>		
		</BaseDataContextProvider>
    </div>
  );
}

export default App;
