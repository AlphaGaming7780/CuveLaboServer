// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { Graph } from './Graph/Graph.tsx';
import { RegisteredUserPanel } from './RegisteredUserPanel/RegisteredUserPanel.tsx';
import { defaultUpdatedValue, UpdatedValueContext, UpdatedValueContextProvider } from './API/UpdatedValue.tsx';
import { BaseDataContext, BaseDataContextProvider, defaultBaseData } from './API/GetBaseData.tsx';
import { useContext } from 'react';


const WaitForData = ({children}) => {
	let data = useContext(BaseDataContext)
	let data2 = useContext(UpdatedValueContext)

	let value = ( data === defaultBaseData || data2 === defaultUpdatedValue )

	return (
		<div className='InApp' style={{display: value ? "none" : "flex" }}> 
			{children}
		</div>
	)

}

function App() {
  return (
    <div className="App">
		<BaseDataContextProvider>
			<UpdatedValueContextProvider>
				<WaitForData>
					<div style={{width:"20%"}}>

					</div>
					<div style={{width:"50%"}}>
						<div style={{width:"100%", height:"25rem"}}>
							<Cuve />
						</div>
						<Graph/>
					</div>
					<div style={{width:"20%"}}>
						<RegisteredUserPanel/>
					</div>
				</WaitForData>
			</UpdatedValueContextProvider>	
		</BaseDataContextProvider>
    </div>
  );
}

export default App;
