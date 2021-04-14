<template>
  <div class="flex justify-between">
    <label v-for="i in [...Array(8).keys()]" class="block">
      <input
          v-model="invite[i]"
          :ref="el => (inputs[i] = el)"
          @focus="focus(i)"
          @input="input"
          @keydown="keydown"
          @paste="paste"
          maxlength="1"
          class="block text-pink-900 w-3ch h-4ch border-b-4 border-pink-400 font-2xl p-2 bg-pink-100 rounded invite-input text-center outline-none transform duration-100 focus:scale-115"
      >
    </label>
  </div>
</template>

<script>
import { onMounted, reactive, ref } from 'vue'

export default {
  name: 'InviteInput',

  props: {
    length: { type: Number, default: 8 }
  },

  setup (props, ctx) {
    const invite = reactive([])
    const inputs = reactive([])
    const size = props.length

    for (let i = 0; i < size; ++i) {
      invite.push('')
      inputs.push(null)
    }

    const focused = ref(null)

    onMounted(() => {
      if (inputs.length === 0) {
        return
      }

      inputs[0].focus()
    })

    const focus = i => {
      focused.value = i
    }

    const input = event => {
      const i = focused.value
      invite[i] = event.target.value.slice(0, 1)
      ctx.emit('update:value', invite.join(''))
      inputs[i + 1 >= size ? size - 1 : i + 1].focus()
    }

    const keydown = event => {
      const i = focused.value
      switch (event.key) {
        case 'Backspace':
          invite[i] = ''
          ctx.emit('update:value', invite.join(''))
          inputs[i - 1 < 0 ? 0 : i - 1].focus()
          break

        case 'Delete':
          invite[i] = ''
          ctx.emit('update:value', invite.join(''))
          break

        case 'ArrowLeft':
          inputs[i - 1 < 0 ? 0 : i - 1].focus()
          break

        case 'ArrowRight':
          inputs[i + 1 >= size ? size - 1 : i + 1].focus()
          break

        default:
          return
      }

      event.preventDefault()
    }

    const paste = event => {
      event.preventDefault()
      const pasted = event.clipboardData
        .getData('text/plain')
        .slice(0, size - focused.value)
        .split('')

      for (let i = focused.value; i < size; ++i) {
        if (i - focused.value in pasted) {
          invite[i] = pasted[i - focused.value]
        }
      }

      ctx.emit('update:value', invite.join(''))
    }

    return {
      invite,
      inputs,
      focus,
      input,
      keydown,
      paste
    }
  }
}
</script>
