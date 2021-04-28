<template>
  <router-view></router-view>
  <div class="clip-paths"></div>
  <waff-modal :open="!cryptoStorageInitialized" :closeable="false">
    <div class="relative">
      <h1 class="text-2xl pb-2 px-8 border-b border-gray-200">Odszyfruj dane przeglądarki</h1>
      <undraw-authentication class="h-72 w-96 absolute top-1/2 left-1/1 transform -translate-x-2/5 -translate-y-1/2" />
      <div class="w-3/4">
        <p class="pt-4 px-8 text-lg text-gray-900">
          Aby kontynuować, musisz odszyfrować dane przeglądarki.
        </p>

        <label class="px-8 block pt-4">
          <div class="text-lg pb-2 text-gray-800">Hasło:</div>
          <input v-model="cryptoPass" type="text" class="w-full border-b-2 border-gray-500 block px-4 py-2" placeholder="xqdMzrXf5BjYBjRp">
        </label>

        <p class="pt-4 px-8 text-sm text-gray-800">
          Jeżeli nie znasz hasła - wpisz nowe, by wygenerować nowe dane.
        </p>

        <div class="px-8 text-pink-600 flex items-center pt-8">
          <i-bi-info-square-fill class="w-8 h-8 mr-5 flex-shrink-0"/>
          Twoje dane są przetrzymywane zaszyfrowane w pamięci przeglądarki.
        </div>

        <div class="px-8 text-pink-600 flex items-center pt-4 pb-12">
          <i-bi-info-square-fill class="w-8 h-8 mr-5 flex-shrink-0"/>
          Nie zapisuj tego hasła w przeglądarce.
        </div>
      </div>

      <div class="flex justify-center absolute w-full left-0 top-1/1 transform -translate-y-1/3">
        <waff-button @click="initCrypto" class="text-2xl" :height="52">Odszyfruj</waff-button>
      </div>
    </div>
  </waff-modal>
</template>

<script>
import { Certificate } from 'pkijs'
import { ref } from 'vue'
import useCryptoStore from './utils/cryptoStore'

export default {
  name: 'App',
  setup () {
    const store = useCryptoStore()
    const cryptoPass = ref('')

    const initCrypto = async () => {
      store.init(cryptoPass.value)
      cryptoPass.value = ''

      const publicKey = await store.get('publicKey')
      if (!publicKey) {

      }
    }

    return {
      cryptoPass,
      initCrypto,

      cryptoStorageInitialized: store.initialized
    }
  }
}
</script>
