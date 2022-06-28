import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import useColors from '../__common/queries/useColors'
import ColorSample from './components/ColorSample'

export default function AppIndex() {
  return (
    <>
      <div className="my-3">
        <Link to="add" className="btn btn-outline-primary">Add color</Link>
      </div>
      <ColorsList />
    </>
  )
}

function ColorsList() {
  const [name, setName] = useState('')
  const [isPrimary, setIsPrimary] = useState('')
  const [red, setRed] = useState('')
  const [green, setGreen] = useState('')
  const [blue, setBlue] = useState('')
  const [ordering, setOrdering] = useState({})

  const { list: { query, data: colors } } = useColors({
    params: {
      projection: 'detail',
      name: name || undefined,
      is_primary: isPrimary || undefined,
      red: red || undefined,
      green: green || undefined,
      blue: blue || undefined,
      ordering: (
        Object.keys(ordering).length ?
          Object.entries(ordering)
            .map(([column, ascending]) => `${ascending ? '' : '-'}${column}`).join(',')
          : undefined
      ),
    },
  })

  return (
    query.isLoading ?

      'Loading...'

      : (
        <div className="table-container">
          <table className="table table-striped table-bordered table-hover">
            <thead>
              <tr>
                <th><input value={name} onChange={(e) => setName(e.target.value)} /></th>
                <th><input value={isPrimary} onChange={(e) => setIsPrimary(e.target.value)} /></th>
                <th><input value={red} onChange={(e) => setRed(e.target.value)} /></th>
                <th><input value={green} onChange={(e) => setGreen(e.target.value)} /></th>
                <th><input value={blue} onChange={(e) => setBlue(e.target.value)} /></th>
                <th></th>
              </tr>

              <tr>
                <th><SortButton ordering={ordering} setOrdering={setOrdering} columnName="name" label="Name" /></th>
                <th><SortButton ordering={ordering} setOrdering={setOrdering} columnName="is_primary" label="Primary?" /></th>
                <th><SortButton ordering={ordering} setOrdering={setOrdering} columnName="red" label="Red" /></th>
                <th><SortButton ordering={ordering} setOrdering={setOrdering} columnName="green" label="Green" /></th>
                <th><SortButton ordering={ordering} setOrdering={setOrdering} columnName="blue" label="Blue" /></th>
                <th>Hex Code</th>
              </tr>
            </thead>

            <tbody>
              {colors?.map(
                color =>
                  <ColorItem key={color.id} color={color} />
              )}
            </tbody>
          </table>

          <div>
            Ordering: {Object.entries(ordering).map(([column, ascending]) => `${ascending ? '' : '-'}${column}`).join(', ') || 'default'}
          </div>
        </div>
      )
  )
}

function SortButton({ ordering, setOrdering, columnName, label }) {
  return (
    <button
      onClick={() => {
        setOrdering(old => {
          let newOrdering = { ...old }

          if (newOrdering[columnName] === true) {
            newOrdering[columnName] = false
          } else if (newOrdering[columnName] === false) {
            delete newOrdering[columnName]
          } else {
            newOrdering[columnName] = true
          }

          return newOrdering
        })
      }}>

      {ordering[columnName] === true ? '+' : ordering[columnName] === false ? '-' : ''}
      {label}

    </button>
  )
}

function ColorItem({ color }) {
  return (
    <tr>
      <td>
        <div className="flex items-center" style={{ gap: '0.5em' }}>
          <ColorSample {...color} />
          <span><Link to={`${color.id}/edit/`}>{color.name}</Link></span>
        </div>
      </td>
      <td>{String(color.is_primary)}</td>
      <td>{color.red}</td>
      <td>{color.green}</td>
      <td>{color.blue}</td>
      <td>{color.hex_code}</td>
    </tr>
  )
}
