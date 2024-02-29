import React, {useEffect, useRef, useState} from 'react'
import {useNavigate, useParams} from 'react-router'
import {Loader} from '../UI/Loader'


export const Result = () => {
  const navigate = useNavigate()
  const params = useParams()

  const button = useRef(null)
  const [bottom, setBottom] = useState(0)
  const [isLoading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [data, setData] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const res = await fetch(
          `https://demo.softeis.net/api/v1/item/${params.name}`,
        )

        const result = await res.json()
        setData(result)
      } catch (e) {
        setError('Товар не найден')
        console.error('Error: ', e)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [params.name])

  useEffect(() => {
    if (button.current) {
      setBottom(button.current.offsetHeight)
    }
  }, [button])

  if (isLoading)
    return (
      <>
        <div
          style={{
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
            paddingTop: '30px',
          }}
        >
          <Loader/>
        </div>
        <div className="result__button" ref={button}>
          <button onClick={() => navigate('/')}>Scan again</button>
        </div>
      </>
    )

  if (error.length !== 0 || !data)
    return (
      <>
        <div
          style={{
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
            paddingTop: '30px',
          }}
        >
          <p className="result__error">{error}</p>
        </div>
        <div className="result__button" ref={button}>
          <button onClick={() => navigate('/scan')}>Scan again</button>
        </div>
      </>
    )

  return (
    <>
      <div className="result" style={{paddingBottom: bottom + 'px'}}>
        <img src={data.image} alt={data.name} className="result__image"/>
        <p className="result__row">
          <span>Name:</span> {data.name}
        </p>
        <p className="result__row">
          <span>Description:</span> {data.description}
        </p>
        <p className="result__row">
          <span>Quantity:</span> {data.stock + ' ' + data.unit}
        </p>
        <p className="result__row">
          <span>Position number:</span> {data.position_number}
        </p>
        <p className="result__row">
          <span>Ean:</span> {data.ean}
        </p>
      </div>
      <div className="result__button" ref={button}>
        <button onClick={() => navigate('/')}>Scan again</button>
      </div>
    </>
  )
}
