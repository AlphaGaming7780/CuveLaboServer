// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { Graph } from './Graph/Graph.tsx';
import { UpdatedValueContextProvider } from './API/UpdatedValue.tsx';
import { BaseDataContext, BaseDataContextProvider, defaultBaseData } from './API/GetBaseData.tsx';
import { useContext } from 'react';


function InApp() {
	let data = useContext(BaseDataContext)

	if(data === defaultBaseData) return <></>

	return (
		<UpdatedValueContextProvider>
			<div style={{width:"50rem", height:"25rem"}}>
				<Cuve />
			</div>
			<Graph/>
		</UpdatedValueContextProvider>		
	)

}

function App() {
  return (
    <div className="App">
		<BaseDataContextProvider>
			{InApp}
		</BaseDataContextProvider>
    </div>
  );
}

export default App;
