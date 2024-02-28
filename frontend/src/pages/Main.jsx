import {useNavigate} from 'react-router'
import {NavBar} from "../components/Header/NavBar";

export const Main = () => {
  const navigate = useNavigate()

  return (
    <>
      <div className="main">
        <button className="main__button" onClick={() => navigate('/scan')}>
          <img
            className="main__img"
            src="/assets/barcode-scan-icon.svg"
            alt="scan"
          />
        </button>
      </div>
    </>
  )
}
