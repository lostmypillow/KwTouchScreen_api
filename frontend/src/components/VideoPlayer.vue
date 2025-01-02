<script setup>
import { ref, onMounted } from "vue";
import { getQueueLength } from "../lib/getQueueLength";
import { fetchVideo } from "../lib/fetchVideo";

const currentVideoIndex = ref(-1);
const videoURL = ref("");
const queueLength = ref([]);

const getVid = async () => {
  if (videoURL.value != "") {
    URL.revokeObjectURL(videoURL.value);
    videoURL.value = "";
  }
  
  queueLength.value = await getQueueLength();
  currentVideoIndex.value =
    currentVideoIndex.value + 1 > queueLength.value - 1
      ? 0
      : currentVideoIndex.value + 1;
  videoURL.value = await fetchVideo(currentVideoIndex.value);
};

onMounted(() => getVid());
</script>
<template>
  <video
    v-if="videoURL != ''"
    class="aspect-w-16 aspect-h-9"
    :src="videoURL"
    @ended="getVid"
    autoplay
  ></video>
  <div
  v-else
    class="shrink-0 aspect-w-16 aspect-h-9 w-full h-[calc(100vw*9/16)] flex items-center jsutify-center"
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
