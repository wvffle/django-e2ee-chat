<template>
  <div class="flex group transform duration-200 cursor-pointer hover:scale-110">
    <div class="btn text-white duration-200 bg-pink-600 group-hover:bg-pink-500 flex items-center" :style="{ height }">
      <div :class="{ 'text-transparent': loading }">
        <slot />
      </div>
      <div v-if="loading" class="flex justify-center items-center absolute inset-0">
        <i-icomoon-free-spinner9 class="w-8 h-8 flex-shrink-0 animate-spin"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Button',
  props: {
    height: { type: Number, default: 36 },
    loading: { type: Boolean, default: false }
  }
}
</script>

<style scoped>
.btn {
  transform: translateZ(0);
  padding: 0 2px;
}

.btn::after, .btn::before {
  background: inherit;
  content: '';
  display: block;
  position: absolute;
  top: 0;
  height: 100%;
  aspect-ratio: 1/1;

}

.btn::before {
  right: calc(100% - 1px);
  border-radius: 0 0 0 100%;
}

.btn::after {
  left: calc(100% - 1px);
  border-radius: 0 100% 0 0;
}
</style>
