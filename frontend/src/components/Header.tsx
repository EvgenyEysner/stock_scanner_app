import { Link } from 'react-router-dom';

interface headerProps {
	isResult: boolean;
}

export const Header = ({ isResult }: headerProps) => {
	return (
		<header className='header'>
			{isResult && (
				<Link to={'/'} style={{ height: 'auto' }}>
					<img src='/src/assets/arrow_back.png' className='header__arrow' />
				</Link>
			)}
		</header>
	);
};
