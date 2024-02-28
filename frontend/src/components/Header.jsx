import { Link } from 'react-router-dom'

export const Header = ( link ) => {
  return (
    <header className="header">
      {link !== '' && (
        <Link to={link} style={{ height: 'auto' }}>
          <img src="/assets/arrow_back.png" className="header__arrow" />
        </Link>
      )}
    </header>
  )
}
