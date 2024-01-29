import { useNavigate } from 'react-router';
import { Header } from '../components/Header';

export const Main = () => {
	const navigate = useNavigate();

	return (
		<>
			<Header link={''} />
			<div className='main'>
				<button className='main__button' onClick={() => navigate('/scan')}>
					<img
						className='main__img'
						src='/src/assets/barcode-scan-icon.svg'
						alt='scan'
					/>
				</button>
			</div>
		</>
	);
};
