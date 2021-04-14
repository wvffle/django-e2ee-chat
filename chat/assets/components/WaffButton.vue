<template>
  <div class="flex group transform duration-200 cursor-pointer hover:scale-110">
    <button-side class="duration-200 fill-pink-600 group-hover:fill-pink-500" :style="{ height, marginRight: -1 }" />
    <div class="text-white duration-200 bg-pink-600 group-hover:bg-pink-500 flex items-center" :style="{ height }">
      <slot />
    </div>
    <button-side class="duration-200 fill-pink-600 group-hover:fill-pink-500" :style="{ height, marginLeft: -1, transform: 'scale(-1, -1)' }" />
  </div>
</template>

<script>
import ButtonSide from '../../public/button-side.svg'
export default {
  name: 'Button',
  components: {
    ButtonSide
  },
  props: {
    height: { type: Number, default: 36 }
  }
}
</script>
