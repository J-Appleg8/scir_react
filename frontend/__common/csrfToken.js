import Cookies from 'js-cookie'

const csrfToken = Cookies.get('csrftoken')

export const csrfTokenHeaders = { headers: { 'X-CSRFToken': csrfToken } }

export default csrfToken