<template>
  <div class="grid grid-cols-5 h-screen bg-blue-gray-50">
    <div class="shadow overflow-hidden bg-white z-10">
      <div class="shadow-md p-4 border-r-4 border-pink-600">
        <div class="grid" style="grid-template-columns: auto calc(100% - 4rem)">
          <div class="w-16 h-16 rounded-full bg-blue-300 flex-shrink-0"></div>
          <div class="pl-4 w-full">
            <div class="text-lg text-gray-700">ox4a66at</div>
            <div class="text-gray-600 truncate">dlugie wiadomosci tez sie ladnie wyswietlaja </div>
          </div>
        </div>
      </div>

      <div class="border-b border-gray-200 p-4">
        <div class="grid" style="grid-template-columns: auto calc(100% - 4rem)">
          <div class="w-16 h-16 rounded-full bg-pink-500 flex-shrink-0"></div>
          <div class="pl-4 w-full">
            <div class="text-lg text-gray-700">aoP86xTu7</div>
            <div class="text-gray-600 truncate">siema</div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-span-4 grid" style="grid-template-rows: 1fr auto">
      <div class="relative">
        <div class="absolute inset-0">
          <undraw-group-chat class="opacity-30 block w-full h-full" preserveAspectRatio="xMidYMid meet" />
        </div>

        <div class="pt-16 px-20">

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-pink-500"></div>
              </div>

              <div class="bg-pink-600 text-white p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                Dziala?
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-blue-300"></div>
              </div>

              <div class="bg-blue-100 text-gray-800 p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                test
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-blue-300"></div>
              </div>

              <div class="bg-blue-100 text-gray-800 p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                o, dziala
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-pink-500"></div>
              </div>

              <div class="bg-pink-600 text-white p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                super
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-pink-500"></div>
              </div>

              <div class="bg-pink-600 text-white p-4 text-sm rounded-tr-3xl rounded-bl-3xl max-w-lg">
                Tenetur tempore nisi ipsam veniam ipsum. Eligendi doloribus atque iure incidunt. Odio qui expedita tenetur pariatur optio. Mollitia iste voluptas ullam labore accusantium. Consectetur ea dolor sit perferendis nisi consequatur. Ad autem mollitia veritatis nihil sint iusto.
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-blue-300"></div>
              </div>

              <div class="bg-blue-100 text-gray-800 p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                dlugie wiadomosci tez sie ladnie wyswietlaja
              </div>
            </div>
          </div>

        </div>

      </div>
      <div class="border-t border-pink-300 flex items-center relative">
        <i-bx-bxs-send class="w-12 h-12 text-pink-600 mx-5 absolute cursor-pointer"/>
        <input type="text" class="pl-22 pr-4 py-4 text-lg block w-full outline-none" placeholder="Napisz wiadomość">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index'
}
</script>
