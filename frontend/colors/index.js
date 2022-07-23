import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AppIndex from './AppIndex';
import AppLayout from './AppLayout';

createRoot(document.getElementById('root')).render(
  <Router basename="colors">
    <Routes>
      <Route path="" element={<AppLayout />}>
        <Route path="" element={<AppIndex />}>
          <Route path=":eventId" element={<AppIndex />} />
        </Route>
      </Route>
    </Routes>
  </Router>
);
