import React from "react";
import {Route, Routes} from "react-router";
import {Scanner} from "./Scanner";
import {Result} from "./Result";
import {Main} from "./Main";
import Container from 'react-bootstrap/Container';

export const Page = () => {
  return (
    <Container>
      <Routes>
        <Route path="/scan" element={<Scanner />} />
        <Route path="/result/:name" element={<Result />} />
        <Route path="*" element={<Main to="/" />} />
      </Routes>
    </Container>
  )
}
