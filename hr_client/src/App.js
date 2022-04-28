import "./App.css";
import { Home } from "./components/Home";

/**
 * method - entrypoint
 */
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Home />
      </header>
    </div>
  );
}

export default App;
