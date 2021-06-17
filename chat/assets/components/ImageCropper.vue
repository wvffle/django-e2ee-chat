<template>
  <div class="flex">
    <div class="mr-4">
      <div class="bg-pink-600 hover:bg-pink-500 text-white rounded p-1 relative">
        <i-ion-upload class="w-6 h-6" />
        <input class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" type="file" @change="loadImage($event)" accept="image/*">
      </div>

      <div class="bg-pink-600 hover:bg-pink-500 text-white rounded p-1 mt-1 cursor-pointer">
        <i-ri-restart-fill @click="reset" class="w-6 h-6" />
      </div>
    </div>

    <div>
      <div v-if="!image.src" class="h-16 w-16 pt-1 pr-1 relative">
        <slot></slot>
      </div>

      <div v-else class="h-16 w-16">
        <cropper
            ref="cropper"
            :src="image.src"
            :auto-zoom="false"
            :resize-image="{ adjustStencil: false }"
            :default-size="{ width: 68, height: 68 }"
            :canvas="{ width: 68, height: 68 }"
            :stencil-size="{ width: 68, height: 68 }"
            :stencil-component="$options.components.CircleStencil"
            :stencil-props="{
              handlers: {},
              movable: false,
              scalable: false,
              aspectRatio: 1,
            }"


            @ready="resetZoom"
            image-restriction="stencil"
            class="h-16 w-16"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import { nextTick, reactive, ref } from 'vue'

export default {
  name: 'ImageCropper',
  components: {
    Cropper, CircleStencil
  },

  setup () {
    const cropper = ref(null)
    const image = reactive({
      type: null,
      src: null
    })

    const getMimeType = (file, fallback = null) => {
      const byteArray = new Uint8Array(file).subarray(0, 4)

      let header = ''

      for (let i = 0; i < byteArray.length; i++) {
        header += byteArray[i].toString(16)
      }

      switch (header) {
        case '89504e47':
          return 'image/png'

        case '47494638':
          return 'image/gif'

        case 'ffd8ffe0':
        case 'ffd8ffe1':
        case 'ffd8ffe2':
        case 'ffd8ffe3':
        case 'ffd8ffe8':
          return 'image/jpeg'

        default:
          return fallback
      }
    }

    const crop = async () => {
      if (!cropper.value) {
        return null
      }

      const { canvas } = cropper.value.getResult()
      return new Promise(resolve => {
        canvas.toBlob(resolve, image.type)
      })
    }

    const reset = () => {
      if (image.src) {
        URL.revokeObjectURL(image.src)
      }

      image.src = null
      image.type = null
    }

    const loadImage = event => {
      const { files } = event.target
      if (files && files[0]) {
        const [file] = files

        if (image.src) {
          URL.revokeObjectURL(image.src)
        }

        const reader = new FileReader()
        reader.onload = async ({ target }) => {
          image.src = URL.createObjectURL(file)
          image.type = getMimeType(target.result, file.type)

          await nextTick()

          cropper.value.refresh()
        }

        reader.readAsArrayBuffer(file)
      }

    }

    const resetZoom = () => {
      cropper.value.zoom(0)
    }
    return {
      cropper,
      image,
      crop,
      reset,
      loadImage,
      resetZoom
    }
  }
}
</script>

<style>
.vue-advanced-cropper__background, .vue-advanced-cropper__foreground {
  background: #fff !important;
  opacity: 1 !important;
}
</style>
