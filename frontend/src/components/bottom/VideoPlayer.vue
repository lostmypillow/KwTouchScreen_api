<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

// Retry configuration
const MAX_RETRIES = 5;
const RETRY_DELAY = 2000; // 2 seconds delay between retries

const fileName = ref("");
const videoURL = computed(() => "http://" + import.meta.env.VITE_VIDEO_URL + "/video/" + fileName.value);
const videoPlayerRef = ref(null);

// Function to retry an action a specified number of times
const retryAction = async (action, retries = MAX_RETRIES) => {
  let attempt = 0;
  while (attempt < retries) {
    try {
      await action(); // Try the action
      return; // If successful, exit
    } catch (error) {
      attempt++;
      console.error(`[VideoPlayer.vue] Attempt ${attempt} failed:`, error);
      if (attempt >= retries) {
        console.error("[VideoPlayer.vue] Max retries reached, stopping.");
        break;
      }
      await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY)); // Wait before retrying
    }
  }
};

const attemptGetNext = () => {
  console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Executing getNext()");
  
  return axios.get("http://" + import.meta.env.VITE_VIDEO_URL + "/next")
    .then(response => {
      if (response.status !== 200 || response.data === null) {
        throw new Error("Failed to get next video or data is null");
      }
      console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Video file name received: ", response.data);

      if (videoPlayerRef.value != null) {
        videoPlayerRef.value.src = '';
        fileName.value = response.data;
        videoPlayerRef.value.src = videoURL.value;
        videoPlayerRef.value.load();
        videoPlayerRef.value.play();
      }
    });
};

const handleError = (event) => {
  // Check if the error is due to unsupported format or MIME type
  if (event.target.error.code === event.target.error.MEDIA_ERR_FORMAT) {
    console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Unsupported video format, retrying...");
    retryAction(attemptGetNext);
  } else {
    console.error("[VideoPlayer.vue] [" + new Date().toISOString() + "] Video playback error: ", event);
    retryAction(attemptGetNext);
  }
};

onMounted(async () => {
  console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Component mounted, calling getNext()");
  await retryAction(attemptGetNext);

  // Attach the error handler to the video element
  if (videoPlayerRef.value) {
    videoPlayerRef.value.addEventListener('error', handleError);
  }
});
</script>

<template>
  <video
    ref="videoPlayerRef"
    class="flex aspect-w-16 aspect-h-9 min-h-[calc(100vw*9/16)]"
    @ended="attemptGetNext()"
    autoplay
  >
    <source :src="videoURL" type="video/mp4" />
  </video>
</template>
