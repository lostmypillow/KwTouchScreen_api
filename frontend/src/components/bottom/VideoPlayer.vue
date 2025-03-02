<script setup>
import { ref, onMounted, watch, computed } from "vue";
import websocketService from "../../lib/websocketService";
import axios from "axios";

const fileName = ref("")

const videoURL = computed(() => "http://" + '192.168.2.17:8004' + "/video/" + fileName.value);

const videoPlayerRef = ref(null);


const getNext = async () => {
  const response = await axios.get('http://' + '192.168.2.17:8004' + "/next");
  if (response.status != 200) {
    console.error(response)
  } else {
    fileName.value = response.data
    videoPlayerRef.value.load()
    videoPlayerRef.value.play()
  }
}
onMounted(async()=>  await getNext())

</script>
<template>
  <video
    ref="videoPlayerRef"
    v-if="fileName != ''"
    class="flex aspect-w-16 aspect-h-9 min-h-[calc(100vw*9/16)]"
    @ended="getNext()"
    autoplay
   >
   <source :src="videoURL" type="video/mp4" />
  </video>
  <div
  v-else
    class="shrink-0 aspect-w-16 aspect-h-9 w-full h-[calc(100vw*9/16)] flex items-center justify-center"
  >
    <ProgressSpinner
      style="width: 50px; height: 50px"
      strokeWidth="8"
      fill="transparent"
      animationDuration=".5s"
      aria-label="Custom ProgressSpinner"
    />
</div>
</template>
