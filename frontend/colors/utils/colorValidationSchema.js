import * as Yup from 'yup'

export default Yup.object().shape({

  name: Yup.string().required().max(20, 'Too long'), // refer to core.models.Color.name.max_length for this value

  is_primary: Yup.boolean(),

  red: Yup.number('Not a valid number')
    .required('Required')
    .min(0, 'Must be in the range of 0 to 255')
    .max(255, 'Must be in the range of 0 to 255'),

  green: Yup.number('Not a valid number')
    .required('Required')
    .min(0, 'Must be in the range of 0 to 255')
    .max(255, 'Must be in the range of 0 to 255'),

  blue: Yup.number('Not a valid number')
    .required('Required')
    .min(0, 'Must be in the range of 0 to 255')
    .max(255, 'Must be in the range of 0 to 255'),

})
