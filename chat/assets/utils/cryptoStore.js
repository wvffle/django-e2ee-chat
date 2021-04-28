import { computed, ref, watch } from 'vue'
import { CryptoStorage } from '@webcrypto/storage'

const cryptoStore = null
export default function useCryptoStore() {
  const store = ref(null)
  const initialized = computed(() => store.value instanceof CryptoStorage)

  const cryptoStore = new Promise(resolve => {
    const stop = watch(() => store, (to, from) => {
      if (to instanceof CryptoStorage && from == null) {
        stop()
        return resolve(to)
      }
    })
  })

  const init = password => {
    store.value = new CryptoStorage(password, 'secure-data')
  }

  const get = async (...args) => {
    const store = await cryptoStore
    return store.get(...args)
  }

  const set = async (...args) => {
    const store = await cryptoStore
    return store.value.set(...args)
  }

  return {
    initialized,
    init,
    get,
    set
  }
}
