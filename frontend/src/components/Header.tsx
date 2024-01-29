import { Link } from 'react-router-dom';

interface headerProps {
	link: string;
}

export const Header = ({ link }: headerProps) => {
	return (
		<header className='header'>
			{link !== '' && (
				<Link to={link} style={{ height: 'auto' }}>
					<img src='/src/assets/arrow_back.png' className='header__arrow' />
				</Link>
			)}
		</header>
	);
};
