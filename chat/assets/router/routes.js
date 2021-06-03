import { state } from '../utils/api'

const component = path => ({ component: async () => {
  if ('__DJANGO_ERROR__' in window) {
    return import('../pages/Error.vue')
  }

  return import(/* @vite-ignore */ path)
}})


export default [
    { name: 'Index', path: '/', ...component('../pages/Index.vue') },
    { name: 'Register', path: '/register', ...component('../pages/Register.vue') },
  ]
