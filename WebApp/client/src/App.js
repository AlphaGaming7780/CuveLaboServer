// import logo from './logo.svg';
import './App.css';
import { Cuve } from './Cuve/Cuve.tsx';
import { Wave } from './Wave/Wave.tsx';

function App() {
  return (
    <div className="App">
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
      </header> */}

        <div style={{width:"50rem", height:"25rem"}}>
          <Cuve />
        </div>


    </div>
  );
}

export default App;
