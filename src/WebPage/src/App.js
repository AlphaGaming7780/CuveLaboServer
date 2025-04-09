// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { Graph } from './Graph/Graph.tsx';
import { UpdatedValueContextProvider } from './API/UpdatedValue.tsx';
import { BaseDataContext, BaseDataContextProvider, defaultBaseData } from './API/GetBaseData.tsx';
import { useContext } from 'react';


const InApp = (children) => {
	// let data = useContext(BaseDataContext)

	// if(data === defaultBaseData) return <></>

	return (
		<>
			{children}
		</>
	)

}

function App() {
  return (
    <div className="App">
		<BaseDataContextProvider>
			<InApp>
				<UpdatedValueContextProvider>
					<div style={{width:"50rem", height:"25rem"}}>
						<Cuve />
					</div>
					<Graph/>
				</UpdatedValueContextProvider>	
			</InApp>
		</BaseDataContextProvider>
    </div>
  );
}

export default App;
