<template>
  <div class="grid grid-cols-5 h-screen bg-blue-gray-50">
    <div class="shadow overflow-hidden bg-white z-10">
      <div class="bg-pink-600 text-white p-4 items-center flex">
        <div class="text-xl">
          {{ profile.name || '&nbsp;' }}
        </div>

        <div class="ml-auto"></div>
        <div @click="addingNewRoom = true" class="bg-pink-500 p-2 rounded-full transform transition duration-200 hover:scale-120 cursor-pointer">
          <i-ri-chat-new-fill class="w-6 h-6" />
        </div>
      </div>
      <div class="relative">
        <input v-model="searchTerm" type="text" class="w-full pl-10 pr-4 py-2 border-b border-pink-600" placeholder="Szukaj pokoju" />
        <i-uil-comment-alt-search class="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-600"/>
      </div>

      <template v-if="profile.lastRooms.length">
        <h2 class="text-lg px-4 pt-4 pb-2 text-gray-400 uppercase text-xs">Ostatnie pokoje</h2>

        <div class="max-w-full px-4 flex overflow-x-auto py-2">
          <!-- TODO [#29]: Add full display name in a tooltip -->
          <div @click="select(room)" v-for="room in profile.lastRooms" class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 flex items-center justify-center text-white text-xs uppercase relative cursor-pointer mr-2 overflow-hidden">
            {{ room?.display_name?.slice(0, 2) }}
            <img class="absolute inset-0 block object-cover w-full h-full" :src="room.image" />
          </div>
        </div>
      </template>

      <h2 class="text-lg px-4 pt-4 text-gray-400 uppercase text-xs">Zaproszenia</h2>

      <div class="border-b border-gray-200 p-4">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0"></div>
          <div class="pl-4 text-gray-700">aoP86xTu7</div>
          <div class="ml-auto"></div>
          <div class="bg-green-400 p-2 rounded-full transform transition duration-200 hover:scale-120 cursor-pointer mr-2">
            <i-ri-chat-check-fill class="w-4 h-4 text-white" />
          </div>
          <div class="bg-red-400 p-2 rounded-full transform transition duration-200 hover:scale-120 cursor-pointer">
            <i-ri-chat-delete-fill class="w-4 h-4 text-white" />
          </div>
        </div>
      </div>

      <h2 class="text-lg px-4 pt-4 pb-2 text-gray-400 uppercase text-xs">Pokoje</h2>

      <div v-for="room of filteredRooms" @click="select(room)" :class="selectedRoom === room ? 'border-pink-600 border-r-4 bg-pink-50' : 'border-gray-200 border-b'" class="p-4 hover:bg-pink-50 cursor-pointer">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 flex items-center justify-center text-white text-xs uppercase relative">
            {{ room?.display_name?.slice(0, 2) }}
            <img class="absolute inset-0 rounded-full block object-cover w-full h-full" :src="room.image" />
          </div>
          <div class="pl-4">
            <div class="text-gray-700">{{ room.display_name }}</div>
            <div class="text-xs text-gray-600 truncate">
              <span>{{ parseEvent(room.lastMessage) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div class="col-span-4 grid" style="grid-template-rows: 1fr auto">
      <div class="relative">
        <div class="absolute inset-0">
          <undraw-group-chat class="opacity-30 block w-full h-full" preserveAspectRatio="xMidYMid meet" />
        </div>

        <div v-if="roomLoading" class="absolute right-8 top-8 items-center text-pink-600 z-20">
          <i-icomoon-free-spinner9 class="w-8 h-8 flex-shrink-0 animate-spin"/>
        </div>

        <div @scroll="infiniteScroll" ref="scrollView" class="pt-16 absolute inset-0 overflow-y-scroll">
          <div class="flex items-center justify-center text-4xl font-bold text-gray-600 h-full relative z-10" v-if="selectedRoom === null">
            Wybierz pokój
          </div>

          <div v-else class="px-20">
            <div v-for="message of selectedRoom?.messages" class="flex mb-2 max-w-full">
              <div v-if="message.type === 'message'" class="mr-auto relative">
                <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                  <!-- TODO [#30]: Add full author name in a tooltip -->
                  <div :class="message.author === profile.name ? 'bg-pink-500' : 'bg-blue-300'" class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white text-xs uppercase relative">
                    {{ message.author.slice(0, 2) }}
                    <!--                  <img class="absolute inset-0 rounded-full block object-cover w-full h-full" :src="message.author_image" />-->
                  </div>
                </div>

                <div :class="message.author === profile.name ? 'text-white bg-pink-600' : 'text-gray-800 bg-blue-100'" class="p-4 text-sm rounded-tr-3xl rounded-bl-3xl max-w-lg">
                  {{ message.data }}
                </div>
              </div>
              <pre v-else>
              {{ message }}
            </pre>
            </div>
          </div>
        </div>
      </div>
      <div class="border-t border-pink-300 flex items-center relative">
        <i-bx-bxs-send @click="send" class="w-12 h-12 text-pink-600 mx-5 absolute cursor-pointer"/>
        <input :disabled="selectedRoom === null" v-model="message" @keyup.enter.prevent="send" type="text" class="pl-22 pr-4 py-4 text-lg block w-full outline-none" placeholder="Napisz wiadomość">
      </div>
    </div>
  </div>
  <waff-modal v-model:open="addingNewRoom">
    <div class="relative">
      <h1 class="text-2xl pb-2 px-8 border-b border-gray-200">Stwórz nowy pokój</h1>
      <div class="pt-4 pb-8">
        <div class="flex items-center">
          <div>
            <image-cropper ref="cropper" class="mr-4">
              <div class="absolute inset-0 rounded-full bg-pink-600 flex items-center justify-center uppercase text-white text-2xl">
                {{ (roomName || 'na').slice(0, 2) }}
              </div>
            </image-cropper>
          </div>

          <input v-model="roomName" class="flex-grow-0 w-full block border-b-2 border-pink-300 focus:border-pink-500 px-4 py-2 outline-none" placeholder="Nazwa pokoju" type="text">
        </div>

      </div>

      <div class="flex justify-center absolute w-full left-0 top-1/1 transform -translate-y-1/3">
        <waff-button @click="createNewRoom" class="text-2xl" :height="52">Stwórz</waff-button>
      </div>
    </div>
  </waff-modal>
</template>

<script>
import { reactive, ref, nextTick, computed } from 'vue'
import useCryptoStore, { abtb64, b64tab } from '../utils/cryptoStore'
import ReconnectingWebSocket from 'reconnecting-websocket'
import axios from 'axios'

export default {
  name: 'Index',
  setup: function () {
    const store = useCryptoStore()

    const message = ref('')
    const selectedRoom = ref(null)
    const roomLoading = ref(false)
    const scrollView = ref(null)
    const searchTerm = ref('')
    const addingNewRoom = ref(false)
    const roomName = ref('')
    const cropper = ref(null)

    const profile = reactive({
      name: null,
      rooms: {},
      lastRooms: []
    })

    const filteredRooms = computed(() => {
      const rooms = Object.values(profile.rooms)
      if (searchTerm.value) {
        return rooms.filter(room => room.display_name.toLowerCase().includes(searchTerm.value.toLowerCase()))
      }
      return rooms
    })

    const parseEvent = ({ type, date, author, data }) => {
      switch (type) {
        case 'message':
          return `${author}: ${data}`
          break

        case 'null':
          return data
          break
      }
    }

    const decryptEvent = async ({ id, date, author, message: data }) => {
      // NOTE: Backend returns null message when there is no message in room
      if (data === null) {
        return { id, type: 'null', date, author, data: '✏️️ Brak wiadomości, zacznij chatować' }
      }

      // Message is not send to us
      if (!(profile.name in data.keys)) {
        return { id, type: 'message', date, author, data: '🔒 Zaszyfrowana wiadomość' }
      }

      const [key, iv] = await Promise.all(
          data.keys[profile.name]
              .split('|')
              .map(b64tab)
              .map(store.decryptPKI)
      ).then(arr => arr.map(abtb64).map(atob).map(b64tab))

      const message = await store.decryptAES(key, iv, b64tab(data.message))

      return {
        id,
        type: 'message',
        date: new Date(date),
        data: message,
        author
      }
    }

    const rws = new ReconnectingWebSocket(`wss://${location.hostname}/ws/chat/test`)
    rws.addEventListener('open', async () => {
      profile.name = await store.get('name')

      rws.send(JSON.stringify({
        type: 'login',
        name: profile.name
      }))
    })

    rws.addEventListener('message', async ({ data: str }) => {
      const data = JSON.parse(str)
      const sv = scrollView.value

      switch (data.type) {
        case 'rooms':
          const rooms = await Promise.all(data.rooms.map(room => (async () => ({
            ...room,
            lastMessage: await decryptEvent(room.last_message),
            messages: []
          }))()))

          for (const room of rooms) {
            profile.rooms[room.name] = room
          }

          if (data.forceSelect) {
            await select(profile.rooms[data.forceSelect])
          }

          return

        case 'room.m':
          // TODO [#26]: Render new unread message
          profile.rooms[data.event.room].last_message = data.event
          const decryptedEvent = await decryptEvent(data.event)
          profile.rooms[data.event.room].lastMessage = decryptedEvent
          profile.rooms[data.event.room].messages.push(decryptedEvent)

          if (sv.scrollHeight - sv.getBoundingClientRect().height - 200 < sv.scrollTop) {
            await nextTick()
            sv.scrollTo(0, sv.scrollHeight)
          }

          break

        case 'room.m.l':
          const room = profile.rooms[data.room]

          if (data.lastEvent === null) {
            room.messages = [
              ...await Promise.all(data.events.reverse().map(decryptEvent))
            ]

            roomLoading.value = false
            await nextTick()
            scrollView.value.scrollTo(0, scrollView.value.scrollHeight)
            break
          }

          if (data.lastEvent !== room.messages[0].id) {
            console.warn(
                `Last message id (${room.messages[0].id}) ` +
                `is not equal requested id (${data.lastEvent})`,
                data
            )

            roomLoading.value = false
            break
          }

          profile.rooms[data.room].messages = [
            ...await Promise.all(data.events.reverse().map(decryptEvent)),
            ...profile.rooms[data.room].messages
          ]

          if ('_infiniteScroll' in selectedRoom.value) {
            await nextTick()
            scrollView.value.scrollTo(
                0,
                scrollView.value.scrollHeight - selectedRoom.value._infiniteScroll
            )
          }


          roomLoading.value = false
          break

        case 'room.c':
          profile.rooms[data.name] = data
          break

        case 'invites':
          break
      }

      console.log(data)
    })

    const select = room => {
      selectedRoom.value = room
      roomLoading.value = true

      const idx = profile.lastRooms.indexOf(room)
      if (~idx) {
        profile.lastRooms.splice(idx, 1)
      }

      profile.lastRooms.unshift(room)

      rws.send(JSON.stringify({
        type: 'room.f',
        room: room.name,
        lastEvent: null
      }))
    }

    const send = async () => {
      if (message.value.trim() === '') {
        return
      }

      const room = selectedRoom.value

      const key = await crypto.subtle.generateKey({
        name: 'AES-CBC',
        length: 256
      }, true, ['encrypt', 'decrypt'])


      const [keyBuf, iv] = await Promise.all([
        crypto.subtle.exportKey('raw', key),
        crypto.getRandomValues(new Uint8Array(16))
      ])

      const encryptedMessage = await store.encryptAES(key, iv, message.value)

      const keys = {}
      await Promise.all(room.participants.map(async ({ name, public_key }) => {
        keys[name] = [
          abtb64(await store.encryptPKI(public_key, abtb64(keyBuf))),
          abtb64(await store.encryptPKI(public_key, abtb64(iv)))
        ].join('|')
      }))

      const { data } = await axios.post('/api/v1/messages/', {
        room: room.name,
        date: +new Date,
        // TODO [#21]: Implement message retention
        retention_seconds: 20,
        message: {
          message: encryptedMessage,
          keys
        }
      })

      // TODO [#27]: Render message sent but not received
      console.log(data)
      message.value = ''
    }

    const infiniteScroll = event => {
      if (!roomLoading.value && event.target.scrollTop <= 2) {
        roomLoading.value = true

        selectedRoom.value._infiniteScroll = event.target.scrollHeight - event.target.scrollTop

        rws.send(JSON.stringify({
          type: 'room.f',
          room: selectedRoom.value.name,
          lastEvent: selectedRoom.value.messages[0].id
        }))
      }
    }

    const createNewRoom = async () => {
      const fd = new FormData()
      const blob = await cropper.value.crop()
      if (blob) {
        fd.append('image', blob)
      }

      fd.append('display_name', roomName.value)

      const { data } = await axios.post('/api/v1/profile/rooms/', fd)
      roomName.value = ''
      cropper.value.reset()
      addingNewRoom.value = false
    }

    return {
      profile,
      selectedRoom,
      message,
      roomLoading,
      scrollView,
      searchTerm,
      filteredRooms,
      addingNewRoom,
      roomName,
      cropper,
      createNewRoom,
      select,
      send,
      parseEvent,
      infiniteScroll,
    }
  }
}
</script>
