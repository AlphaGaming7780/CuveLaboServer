// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { Graph } from './Graph/Graph.tsx';
import { RegisteredUserPanel } from './RegisteredUserPanel/RegisteredUserPanel.tsx';
import { defaultUpdatedValue, UpdatedValueContext, UpdatedValueContextProvider } from './API/UpdatedValue.tsx';
import { BaseDataContext, BaseDataContextProvider, defaultBaseData } from './API/GetBaseData.tsx';
import { useContext } from 'react';
import { defaultUpdatedClientData, UpdatedClientDataContext, UpdatedClientDataContextProvider } from './API/ClientAPI.tsx';
import { IsAdminContextProvider } from './API/Admin.tsx';


const WaitForData = ({children}) => {
	let data = useContext(BaseDataContext)
	let data2 = useContext(UpdatedValueContext)
	let data3 = useContext(UpdatedClientDataContext)

	let value = ( data === defaultBaseData || data2 === defaultUpdatedValue || data3 === defaultUpdatedClientData )

	if (value) {
		document.title = "Loading..."
	} else {
		if(data.numberOfCuve === 1) document.title = "Carapuce - WebApp"
		else if(data.numberOfCuve === 2) document.title = "Herbizarre - WebApp"
		else if(data.numberOfCuve === 3) document.title = "Tortank - WebApp"
		else document.title = "Unknown - WebApp"
	}

	return (
		<div className='InApp' style={{display: value ? "none" : "flex" }}> 
			{children}
		</div>
	)

}

function App() {
  return (
    <div className="App">
		<IsAdminContextProvider>
			<BaseDataContextProvider>
				<UpdatedValueContextProvider>
					<UpdatedClientDataContextProvider>
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
					</UpdatedClientDataContextProvider>
				</UpdatedValueContextProvider>	
			</BaseDataContextProvider>
		</IsAdminContextProvider>
    </div>
  );
}

export default App;
