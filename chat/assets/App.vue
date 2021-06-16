<template>
  <error v-if="error" />
  <router-view v-else v-slot="{ Component, route }">
    <transition :name="route.meta.transitionName">
      <component :is="Component" :key="route.path" />
    </transition>
  </router-view>

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
import { useToast } from 'vue-toastification'
import { ref } from 'vue'
import useCryptoStore from './utils/cryptoStore'
import { useAPI } from './utils/api'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup () {
    const toast = useToast()
    const store = useCryptoStore()
    const api = useAPI()
    const router = useRouter()

    const cryptoPass = ref('')
    const loading = ref(false)

    const initCrypto = async () => {
      if (cryptoPass.value === '') {
        toast.error("Haslo nie moze byc puste.")
        return
      }

      loading.value = true
      switch (await store.init(cryptoPass.value).catch(err => (console.error(err), false))) {
        case undefined:
          toast.info('Nie znaleziono profilu')
          loading.value = false
          return router.replace('/register')

        case false:
          toast.error('Wystapil blad podczas rozszyfrowywania lokalnych danych przegladarki')
          cryptoPass.value = ''
          loading.value = false
          break

        default:
          if (await api.login()) {
            cryptoPass.value = ''

            toast.success('Zalogowano.', { timeout: 2000 })
            loading.value = false
            return router.replace('/')
          }
      }
    }

    return {
      cryptoPass,
      initCrypto,
      cryptoStorageInitialized: store.initialized,
      loading,
      error: '__DJANGO_ERROR__' in window
    }
  }
}
</script>

<style>
.Vue-Toastification__toast {
  border-radius: 1rem 0 1rem 0 !important;
}

.slide-left-enter-active, .slide-left-leave-active,
.slide-right-enter-active, .slide-right-leave-active {
  transition: transform .2s ease, opacity .2s ease;
}

.slide-left-enter-from, .slide-right-leave-to {
  transform: translateX(-15px);
  opacity: 0;
}

.slide-right-enter-from, .slide-left-leave-to {
  transform: translateX(15px);
  opacity: 0;
}

.flip-list-move {
  transition: transform .2s ease-out;
}

.list-enter-active,
.list-leave-active {
  transition: all 1s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
