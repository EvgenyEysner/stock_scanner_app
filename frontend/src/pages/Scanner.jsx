import React from 'react'
import BarcodeScannerComponent from 'react-qr-barcode-scanner'
import {useNavigate} from 'react-router'

export const Scanner = () => {
  const navigate = useNavigate()

  return (
    <>
      <h1>Scan barcode</h1>
      <div className="scanner">
        <BarcodeScannerComponent
          onUpdate={(_err, result) => {
            if (result) navigate(`/result/${result.getText()}`)
          }}
        />
      </div>
    </>
  )
}
