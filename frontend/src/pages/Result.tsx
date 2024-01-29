import React, { useEffect, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Loader } from '../UI/Loader';
import { Header } from '../components/Header';

interface IProduct {
	id: number;
	name: string;
	description: string;
	image: string;
	unit: number;
	stock: number;
	ean: number | string;
	position_number: number;
	barcode: number;
}

export const Result: React.FC = () => {
	const navigate = useNavigate();
	const params = useParams();
	console.log(params);

	const button = useRef<HTMLDivElement>(null);
	const [bottom, setBottom] = useState(0);
	const [isLoading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [data, setData] = useState<IProduct | null>(null);

	useEffect(() => {
		const fetchData = async () => {
			setLoading(true);
			try {
				const res = await fetch(
					`http://localhost:8000/api/v1/item/${params.name}`
				);
				const result: IProduct = await res.json();
				setData(result);
			} catch (e) {
				setError('Товар не найден');
				console.error('Error: ', e);
			} finally {
				setLoading(false);
			}
		};

		fetchData();
	}, [params.name]);

	useEffect(() => {
		if (button.current) {
			setBottom(button.current.offsetHeight);
		}
	}, [button]);

	if (isLoading)
		return (
			<>
				<Header link={'/scan'} />
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

	if (error.length !== 0 || !data)
		return (
			<>
				<Header link={'/scan'} />
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
					<button onClick={() => navigate('/scan')}>Scan again</button>
				</div>
			</>
		);

	return (
		<>
			<Header link={'/scan'} />
			<div className='result' style={{ paddingBottom: bottom + 'px' }}>
				<img src={data.image} alt={data.name} className='result__image' />
				<p className='result__row'>
					<span>Name:</span> {data.name}
				</p>
				<p className='result__row'>
					<span>Description:</span> {data.description}
				</p>
				<p className='result__row'>
					<span>Quantity:</span> {data.stock + ' ' + data.unit}
				</p>
				<p className='result__row'>
					<span>Position number:</span> {data.position_number}
				</p>
				<p className='result__row'>
					<span>Ean:</span> {data.ean}
				</p>
				{/* <img src={data.barcode} alt={data.name} className='result__image' /> */}
			</div>
			<div className='result__button' ref={button}>
				<button onClick={() => navigate('/')}>Scan again</button>
			</div>
		</>
	);
};
