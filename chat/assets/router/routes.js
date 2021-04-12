const component = path => ({
  component: ('__DJANGO_ERROR__' in window)
    ? () => import('../pages/Error.vue')
    : () => import(path)
})

export default [
    { name: 'Index', path: '/', ...component('../pages/Index.vue') },
  ]
