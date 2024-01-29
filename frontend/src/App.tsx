import { Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import { Main } from './pages/Main';
import { Result } from './pages/Result';
import { Scanner } from './pages/Scanner';

function App() {
	return (
		<Routes>
			<Route path='/' element={<Main />} />
			<Route path='/scan' element={<Scanner />} />
			<Route path='/result/:name' element={<Result />} />

			<Route path='*' element={<Navigate to='/' />} />
		</Routes>
	);
}

export default App;
