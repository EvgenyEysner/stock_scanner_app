import React from 'react';
import BarcodeScannerComponent from 'react-qr-barcode-scanner';
import { useNavigate } from 'react-router-dom';
import { Header } from '../components/Header';

export const Scanner: React.FC = () => {
	const navigate = useNavigate();

	return (
		<>
			<Header isResult={false} />
			<h1>Scan barcode</h1>
			<div className='scanner'>
				<BarcodeScannerComponent
					onUpdate={(_err, result) => {
						if (result) navigate(`/result/${result.text}`);
					}}
				/>
			</div>
		</>
	);
};
