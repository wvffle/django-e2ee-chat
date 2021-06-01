import { computed, ref, watch } from 'vue'
import { CryptoStorage } from '@webcrypto/storage'

const store = ref(null)

export default function useCryptoStore() {
  const initialized = computed(() => store.value instanceof CryptoStorage)

  const cryptoStore = new Promise(resolve => {
    if (initialized.value) {
      return store.value
    }

    const stop = watch(store, (to, from) => {
      if (to instanceof CryptoStorage && from == null) {
        stop()
        return resolve(to)
      }
    })
  })

  const init = async password => {
    store.value = new CryptoStorage(password, 'secure-data')

    try {
      await store.value.get('publicKey')
      return get('name')
    } catch (e) {
      const { privateKey, publicKey } = await crypto.subtle.generateKey(
        {
          name: 'RSA-OAEP',
          modulusLength: 2048,
          publicExponent: new Uint8Array([1, 0, 1]),
          hash: { name: 'SHA-512' }
        },
        true,
        ['encrypt', 'decrypt']
      )

      // Note: Maybe it's worth wrapping key using https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/wrapKey
      await Promise.all([
        crypto.subtle.exportKey('pkcs8', privateKey).then(abtb64).then(k => store.value.set('privateKey', k)),
        crypto.subtle.exportKey('spki', publicKey).then(abtb64).then(k => store.value.set('publicKey', k))
      ])

      return get('name')
    }
  }

  const get = async (key) => {
    const store = await cryptoStore

    // NOTE: We're disallowing the return of private key
    if (key === 'privateKey')  {
      return undefined
    }

    try {
      return store.get(key)
    } catch (e) {
      return undefined
    }
  }

  const set = async (key, value) => {
    const store = await cryptoStore
    return store.set(key, value)
  }

  const encryptPKI = async (publicKey, data) => {
    return crypto.subtle.encrypt('RSA-OAEP', publicKey, data)
  }

  const decryptPKI = async (data) => {
    const privateKey = await crypto.subtle.importKey(
      'pkcs8',
      b64tab(await store.value.get('privateKey')),
      'RSA-OAEP',
      false,
      ['decrypt']
    )

    return crypto.subtle.encrypt('RSA-OAEP', privateKey, data)
  }

  return {
    initialized,
    init,
    get,
    set,
    encryptPKI,
    decryptPKI,
  }
}

export const abtb64 = buf => {
  return btoa(String.fromCharCode.apply(null, new Uint8Array(buf)))
}

export const b64tab = b64 => {
  return Uint8Array.from(atob(b64).split('').map(k => k.charCodeAt(0))).buffer
}
