const component = path => ({ component: () => {
  if ('__DJANGO_ERROR__' in window) {
    return import('../pages/Error.vue')
  }

  if (!localStorage.publicKey) {
    return import('../pages/Register.vue')
  }

  return import(/* @vite-ignore */ path)
}})


export default [
    { name: 'Index', path: '/', ...component('../pages/Index.vue') },
  ]
