import React from 'react'

export default function ColorSample({ red, green, blue }) {
  return (
    <div style={{
      width: 25,
      height: 25,
      borderRadius: 3,
      border: '1px solid rgba(0,0,0, 0.2)',
      backgroundColor: `rgb(${red}, ${green}, ${blue})`,
    }}></div>
  )
}