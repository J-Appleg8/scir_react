import axios from 'axios'
import { Field, Form, Formik } from 'formik'
import React from 'react'
import { useMutation, useQueryClient } from 'react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import LabeledFieldWithErrors from '../../__common/components/LabeledFieldWithErrors'
import { csrfTokenHeaders } from '../../__common/csrfToken'
import useColors from '../../__common/queries/useColors'
import ColorSample from '../components/ColorSample'
import colorValidationSchema from '../utils/colorValidationSchema'

export default function EditColor() {
  const { colorId: id } = useParams()

  const { detail } = useColors()
  const { query, data: color } = detail(id)

  return query.isLoading ?
    'Loading...'
    : <EditColorForm color={color} />
}

function EditColorForm({ color }) {
  const { colorId: id } = useParams()

  const queryClient = useQueryClient()

  const navigate = useNavigate()

  const mutation = useMutation(
    (formData) => axios.put(`/api/v1/colors/${id}/`, formData, csrfTokenHeaders),
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
      initialValues={color}
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
              gridTemplateColumns: '3fr auto 1fr 1fr 1fr auto',
              gap: '1em',
            }}>

            {/* try entering more than 20 characters here */}
            <LabeledFieldWithErrors
              label="Name"
              name="name"
            />

            <label htmlFor="is_primary">Is Primary Color?</label>
            <div className="flex items-center justify-center">
              <Field
                type="checkbox"
                id="is_primary"
                name="is_primary"
              />
            </div>

            <LabeledFieldWithErrors
              label="Red"
              name="red"
              type="number"
              min="0"
              max="255"
            />

            {/* try entering text in this field */}
            <LabeledFieldWithErrors
              label="Green"
              name="green"
              // type="number"
              min="0"
              max="255"
            />

            {/* try entering a number outside of 0-255: */}
            <LabeledFieldWithErrors
              label="Blue"
              name="blue"
              type="number"
            // min="0"
            // max="255"
            />

            <label>Color Sample</label>
            <ColorSample {...values}
            />
          </fieldset>

          <div className="mt-8 border-t border-t-zinc-100 pt-3 flex justify-between">
            <div>
              <DeleteButton color={color} />
            </div>

            <div className="flex" style={{ gap: '0.5em' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={Object.keys(errors).length || !dirty}
              >
                Save
              </button>

              <Link
                to="/"
                className="btn btn-outline-primary">
                Cancel
              </Link>
            </div>
          </div>

          {/* <div>
            {Object.values(errors).length ?
              <pre>{JSON.stringify(errors)}</pre>
              : 'No errors'}
          </div> */}

          {/* <pre>{JSON.stringify({ values, errors, ...props }, null, 2)}</pre> */}
        </Form>
      )}

    </Formik>
  )
}

function DeleteButton({ color }) {
  const queryClient = useQueryClient()

  const navigate = useNavigate()

  const mutation = useMutation(
    () => axios.delete(`/api/v1/colors/${color.id}/`, csrfTokenHeaders),
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

  function handleClick(e) {
    if (confirm(`Are you sure you want to delete the color ${color.name}?`)) {
      mutation.mutate()
    }
  }

  return (
    <button
      type="button"
      className="btn btn-outline-danger"
      onClick={handleClick}>
      Delete
    </button>
  )
}
