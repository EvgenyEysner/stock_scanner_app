import React from "react";

export const Footer = () => {
  return (
    <footer data-bs-theme="dark" className="bg-body-tertiary text-center text-lg-start fixed-bottom">
      <div className="text-center p-3">
        <p className="text-white">&copy; {new Date().getFullYear()} All rights reserved</p>
        <a className="text-body text-white text-decoration-none" href="https://softeis.net/">SoftEis</a>
      </div>
    </footer>
  )
}
