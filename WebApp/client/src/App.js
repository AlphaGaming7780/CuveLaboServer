// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Tortank/Cuve/Cuve.tsx';
import { WaterLevelContextProvider } from './API.tsx';

function App() {

  return (
    <div className="App">
      	<WaterLevelContextProvider>
			{/* <header className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<p>
					Edit <code>src/App.js</code> and save to reload.
					</p>
					<a
					className="App-link"
					href="https://reactjs.org"
					target="_blank"
					rel="noopener noreferrer"
					>
					Learn React
					</a>
				</header> */
			}

			<div style={{width:"50rem", height:"25rem"}}>
				<Cuve />
			</div>    
      	</WaterLevelContextProvider>
    </div>
  );
}

export default App;
