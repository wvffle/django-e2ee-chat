<template>
  <div class="flex group transform duration-200 cursor-pointer hover:scale-110">
    <div class="btn text-white duration-200 bg-pink-600 group-hover:bg-pink-500 flex items-center" :style="{ height }">
      <slot />
    </div>
  </div>
</template>

<script>
// TODO [#15]: Add loading state
export default {
  name: 'Button',
  props: {
    height: { type: Number, default: 36 }
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
