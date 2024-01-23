import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader } from '../UI/Loader';
import { Header } from '../components/Header';

export const Result: React.FC = () => {
	const navigate = useNavigate();
	const button = useRef<HTMLDivElement>(null);
	const [bottom, setBottom] = useState(0);
	const [isLoading, setLoading] = useState(true);
	const [error, setError] = useState('');

	useEffect(() => {
		// Здесь должен быть запрос на сервер

		// setTimeout(() => {
		setLoading(false);
		// }, 2000);
	}, []);

	useEffect(() => {
		if (button.current) {
			setBottom(button.current.offsetHeight);
		}
	}, [button]);

	const data = {
		id: 2,
		name: 'Test',
		description: 'Description this item',
		image:
			'https://upload.wikimedia.org/wikipedia/commons/5/5a/Books_HD_%288314929977%29.jpg',
		unit: 1,
		stock: 10,
		ean: '0123456789789',
		position_number: 120,
		barcode:
			'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXW1Gu4d-HdFxRRkpbor-Ygchfktf8nfzgE5IOfosAyg&s',
	};

	if (isLoading)
		return (
			<>
				<Header isResult={true} />
				<div
					style={{
						width: '100%',
						display: 'flex',
						justifyContent: 'center',
						paddingTop: '30px',
					}}
				>
					<Loader />
				</div>
				<div className='result__button' ref={button}>
					<button onClick={() => navigate('/')}>Scan again</button>
				</div>
			</>
		);

	if (error.length !== 0)
		return (
			<>
				<Header isResult={true} />
				<div
					style={{
						width: '100%',
						display: 'flex',
						justifyContent: 'center',
						paddingTop: '30px',
					}}
				>
					<p className='result__error'>{error}</p>
				</div>
				<div className='result__button' ref={button}>
					<button onClick={() => navigate('/')}>Scan again</button>
				</div>
			</>
		);

	return (
		<>
			<Header isResult={true} />
			<div className='result' style={{ paddingBottom: bottom + 'px' }}>
				<img src={data.image} alt={data.name} className='result__image' />
				<p className='result__row'>
					<span>Name:</span> {data.name}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<img src={data.barcode} alt={data.name} className='result__image' />
			</div>
			<div className='result__button' ref={button}>
				<button onClick={() => navigate('/')}>Scan again</button>
			</div>
		</>
	);
};
