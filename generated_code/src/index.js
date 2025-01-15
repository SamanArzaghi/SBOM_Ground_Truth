import ReactDOM from 'react-dom';
import App from './components/App';

// Entry point of the application
// This file is responsible for rendering the main App component into the DOM.
// It assumes that there is an HTML element with the id 'root' where the app will be mounted.
// Ensure that 'react-dom' is included in your project's dependencies in package.json.

const rootElement = document.getElementById('root');
if (rootElement) {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    rootElement
  );
} else {
  console.error("Root element not found. Please ensure there is an element with id 'root' in your HTML.");
}