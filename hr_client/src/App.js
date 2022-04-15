import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <button
          onClick={() => {
            fetch("/api/roles/");
          }}
        >
          Click me
        </button>
      </header>
    </div>
  );
}

export default App;
