<template>
  <div v-if="open" ref="overlay" @click="closeOverlay" class="fixed inset-0 z-100 bg-black bg-opacity-80 flex justify-center items-center">
    <div class="w-full max-w-xl bg-white rounded shadow p-4">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'WaffModal',
  props: {
    open: { type: Boolean, required: true },
    overlayCloses: { type: Boolean, default: true },
    closeable: { type: Boolean, default: true }
  },
  emits: ['update:open'],
  setup (props, ctx) {
    const overlay = ref(null)

    const close = () => {
      if (props.closeable) {
        ctx.emit('update:open', false)
      }
    }

    const closeOverlay = event => {
      if (event.target === overlay.value && props.overlayCloses) {
        return close()
      }
    }

    return {
      close,
      closeOverlay,
      overlay
    }
  }
}
</script>
