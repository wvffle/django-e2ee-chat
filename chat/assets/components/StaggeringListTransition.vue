<template>
<transition-group
    name="staggered-fade"
    tag="div"
    :css="false"
    @before-enter="beforeEnter"
    @enter="enter"
    @leave="leave"
  >
  <slot />
</transition-group>
</template>

<script setup>
import gsap from 'gsap'

const heightMap = new Map()

const beforeEnter = el => {
  if (heightMap.has(el)) {
    el.style.opacity = 0
    el.style.height = 0
  }
}

const enter = (el, done) => {
  heightMap.set(el, el.getBoundingClientRect().height)
  gsap.to(el, {
    opacity: 1,
    height: heightMap.get(el),
    delay: el.dataset.index * 0.15,
    onComplete: done
  })
}

const leave = (el, done) => {
  console.log(el, el.getBoundingClientRect())
  gsap.to(el, {
    opacity: 0,
    height: 0,
    delay: el.dataset.index * 0.15,
    onComplete: done
  })
}
</script>

<style scoped>

</style>
