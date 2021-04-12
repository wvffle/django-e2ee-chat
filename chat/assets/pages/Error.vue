<template>
  <div>
    {{ status }}
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'Error',
  setup () {
    return window.__DJANGO_ERROR__
  }
}
</script>
