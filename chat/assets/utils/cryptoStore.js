import { ref, watch } from 'vue'
import { CryptoStorage } from '@webcrypto/storage'

const encoder = new TextEncoder()

const store = ref(null)
const ALGORITHM = {
  name: 'RSA-OAEP',
  modulusLength: 2048,
  publicExponent: new Uint8Array([1, 0, 1]),
  hash: { name: 'SHA-512' }
}

const initialized = ref(false)

const cryptoStore = new Promise(resolve => {
  if (store.value instanceof CryptoStorage) {
    return store.value
  }

  const stop = watch(store, (to, from) => {
    if (to instanceof CryptoStorage && from == null) {
      stop()
      return resolve(to)
    }
  })
})

const PUBLIC_KEY_INITIALIZATION_ERROR = new Error('Public key initialization failed')

export default function useCryptoStore() {
  const init = async password => {
    const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password))
    store.value = new CryptoStorage(password, new TextDecoder().decode(hash))

    try {
      if (await store.value.get('publicKey') === undefined) {
        throw PUBLIC_KEY_INITIALIZATION_ERROR
      }

      initialized.value = true
      return get('name')
    } catch (e) {
      if (e !== PUBLIC_KEY_INITIALIZATION_ERROR) {
        console.error(e)
      }

      const { privateKey, publicKey } = await crypto.subtle.generateKey(
        ALGORITHM,
        true,
        ['encrypt', 'decrypt']
      )

      // Note: Maybe it's worth wrapping key using https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/wrapKey
      await Promise.all([
        crypto.subtle.exportKey('pkcs8', privateKey).then(abtb64).then(k => set('privateKey', k)),
        crypto.subtle.exportKey('spki', publicKey).then(abtb64).then(k => set('publicKey', k))
      ])

      initialized.value = true
      return get('name')
    }
  }

  const deauth = async () => {
    store.value = null
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

  const encryptPKI = async (key, data) => {
    const publicKey = await crypto.subtle.importKey(
      'spki',
      b64tab(key),
      ALGORITHM,
      true,
      ['encrypt']
    )

    return crypto.subtle.encrypt({ name: ALGORITHM.name }, publicKey, encoder.encode(data))
  }

  const decryptPKI = async (data) => {
    const privateKey = await crypto.subtle.importKey(
      'pkcs8',
      b64tab(await store.value.get('privateKey')),
      ALGORITHM,
      true,
      ['decrypt']
    )

    return crypto.subtle.decrypt({ name: ALGORITHM.name }, privateKey, new Uint8Array(data))
  }

  const decryptAES = async (key, iv, data) => {
    const aesKey = await crypto.subtle.importKey("raw", key, "AES-CBC", false, ['decrypt'])
    const buf = await crypto.subtle.decrypt({ name: 'AES-CBC', iv }, aesKey, data)
    return atob(abtb64(buf))
  }

  const encryptAES = async (key, iv, data) => {
    if (key instanceof ArrayBuffer) {
      key = await crypto.subtle.importKey("raw", key, "AES-CBC", false, ['encrypt'])
    }

    const buf = await crypto.subtle.encrypt({ name: 'AES-CBC', iv }, key, encoder.encode(data))
    return abtb64(buf)
  }

  return {
    initialized,
    init,
    get,
    set,
    encryptPKI,
    decryptPKI,
    encryptAES,
    decryptAES,
    deauth,
  }
}

export const abtb64 = buf => {
  return btoa(String.fromCharCode.apply(null, new Uint8Array(buf)))
}

export const b64tab = b64 => {
  const str = atob(b64)
  const buf = new ArrayBuffer(str.length)
  const bufView = new Uint8Array(buf)

  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i)
  }

  return buf
}
