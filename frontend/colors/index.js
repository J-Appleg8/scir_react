import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import AppIndex from './AppIndex'
import AppLayout from './AppLayout'
import AddColor from './routes/AddColor'
import EditColor from './routes/EditColor'

ReactDOM.render(
  <Router basename="colors">
    <Routes>
      <Route path="" element={<AppLayout />}>
        <Route index element={<AppIndex />} />

        <Route path="add" element={<AddColor />} />

        <Route path=":colorId">
          <Route path="edit" element={<EditColor />} />
        </Route>
      </Route>
    </Routes>
  </Router>,
  document.getElementById('root')
)
