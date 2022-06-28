import { Field, useFormikContext } from 'formik'
import React from 'react'

export default function LabeledFieldWithErrors({ label, name, ...props }) {
  const { errors } = useFormikContext()

  return (
    <>
      <label htmlFor={name}>{label}</label>
      <div>
        <Field
          id={name}
          name={name}
          {...props}
        />

        {errors[name] &&
          <small className="text-danger">{errors[name]}</small>}
      </div>
    </>
  )
}
