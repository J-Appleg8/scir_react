import axios from 'axios'
import { Field, Form, Formik } from 'formik'
import React from 'react'
import { useMutation, useQueryClient } from 'react-query'
import { Link, useNavigate } from 'react-router-dom'
import { csrfTokenHeaders } from '../../__common/csrfToken'
import ColorSample from '../components/ColorSample'
import colorValidationSchema from '../utils/colorValidationSchema'

export default function AddColor() {
  const queryClient = useQueryClient()

  const navigate = useNavigate()

  const mutation = useMutation(
    (formData) => axios.post(`/api/v1/colors/`, formData, csrfTokenHeaders),
    {
      onError: ({ response: { status, statusText, data: { detail } } }) => {
        alert(`${status} ${statusText}: ${detail}`)
      },
      onSuccess: () => {
        queryClient.invalidateQueries(['colors'])
        navigate('/')
      },
    }
  )

  return (
    <Formik
      initialValues={{}}
      validationSchema={colorValidationSchema}
      onSubmit={mutation.mutate}
    >

      {({ values, errors, dirty, isSubmitting, ...props }) => (
        <Form>

          <fieldset
            disabled={isSubmitting}
            style={{
              display: 'grid',
              gridAutoFlow: 'column',
              gridTemplateRows: 'auto auto',
              gap: '1em',
            }}>

            <label>Name</label>
            <Field
              name="name"
              placeholder="Gold"
            />

            <label>Is Primary Color?</label>
            <Field
              name="is_primary"
              type="checkbox"
            />

            <label>Red</label>
            <Field
              name="red"
              type="number"
              min="0"
              max="255"
              placeholder="255"
            />

            <label>Green</label>
            <Field
              name="green"
              type="number"
              min="0"
              max="255"
              placeholder="215"
            />

            <label>Blue</label>
            <Field
              name="blue"
              type="number"
              min="0"
              max="255"
              placeholder="0"
            />

            <label>Color Sample</label>
            <ColorSample {...values} />
          </fieldset>

          <div className="mt-8 flex justify-end" style={{ gap: '0.5em' }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={Object.keys(errors).length || !dirty}
            >
              Add color
            </button>
            <Link to="/" className="btn btn-outline-primary">Cancel</Link>
          </div>

          {/* <pre>{JSON.stringify({ values, errors, ...props }, null, 2)}</pre> */}
        </Form>
      )}

    </Formik>
  )
}
