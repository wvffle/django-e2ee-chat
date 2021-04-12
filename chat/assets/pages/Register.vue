<template>
  <div class="grid grid-cols-2 bg-pink-400">
    <div></div>
    <div class="flex items-center justify-center">
      <unlock-svg></unlock-svg>
    </div>
  </div>
</template>

<script>
import UnlockSvg from '../../public/images/undraw_unlock_24mb.svg'
export default {
  name: 'Register',

  components: {
    UnlockSvg
  },

  setup () {
    return {

    }
  }
}
</script>
