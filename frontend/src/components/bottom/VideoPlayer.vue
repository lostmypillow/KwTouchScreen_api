<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import axios from "axios";

const RETRY_DELAY = 2000;
const CHECK_INTERVAL = 1000; // Interval to check for stalling

const fileName = ref("");
const videoURL = computed(() => "http://" + import.meta.env.VITE_VIDEO_URL + "/video/" + fileName.value);
const videoPlayerRef = ref(null);

let stopped = false;
let retryInProgress = false;
let abortController = null;
let inactivityTimeout = null;
let stallCheckInterval = null;
let lastTime = 0;

const retryAction = async (action) => {
  if (retryInProgress) {
    console.log("[VideoPlayer.vue] Retry already in progress, skipping...");
    return;
  }

  console.log("[VideoPlayer.vue] Starting retryAction...");
  retryInProgress = true;

  while (!stopped) {
    try {
      if (abortController) {
        console.log("[VideoPlayer.vue] Aborting previous request...");
        abortController.abort();
      }

      abortController = new AbortController();
      console.log("[VideoPlayer.vue] Executing action...");
      await action(abortController.signal);
      console.log("[VideoPlayer.vue] Action successful, exiting retry loop");
      retryInProgress = false;
      return;
    } catch (error) {
      if (axios.isCancel(error)) {
        console.warn("[VideoPlayer.vue] Request aborted, skipping retry...");
        retryInProgress = false;
        return;
      }

      console.error("[VideoPlayer.vue] Retry failed:", error);
      console.log("[VideoPlayer.vue] Waiting before retry...");
      await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
    }
  }

  console.log("[VideoPlayer.vue] Stopped flag detected, ending retryAction");
  retryInProgress = false;
};

const attemptGetNext = async (signal) => {
  console.log("[VideoPlayer.vue] [" + new Date().toISOString() + "] Executing getNext()");
  
  try {
    const response = await axios.get(
      "http://" + import.meta.env.VITE_VIDEO_URL + "/next",
      { signal }
    );

    console.log("[VideoPlayer.vue] Response received:", response);

    if (response.status !== 200 || response.data === null) {
      console.error("[VideoPlayer.vue] Failed to get next video or data is null");
      throw new Error("Failed to get next video or data is null");
    }

    console.log("[VideoPlayer.vue] Video file name received:", response.data);

    if (videoPlayerRef.value) {
      console.log("[VideoPlayer.vue] Updating video player source...");
      videoPlayerRef.value.src = '';
      fileName.value = response.data;
      videoPlayerRef.value.src = videoURL.value;
      videoPlayerRef.value.load();
      videoPlayerRef.value.play();
    }
  } catch (error) {
    console.error("[VideoPlayer.vue] Error in attemptGetNext:", error);
    throw error;
  }
};

// Handle stalled or interrupted playback
const handleStall = () => {
  console.warn("[VideoPlayer.vue] Detected stall — retrying...");
  retryAction(attemptGetNext);
};

const handleError = (event) => {
  console.error("[VideoPlayer.vue] Video playback error:", event);
  retryAction(attemptGetNext);
};

// Detect inactivity or stalling
const setupInactivityWatch = () => {
  console.log("[VideoPlayer.vue] Setting up inactivity watch...");
  if (inactivityTimeout) {
    console.log("[VideoPlayer.vue] Clearing existing inactivity timeout");
    clearTimeout(inactivityTimeout);
  }

  inactivityTimeout = setTimeout(() => {
    console.warn("[VideoPlayer.vue] Detected inactivity — retrying...");
    retryAction(attemptGetNext);
  }, 5000);
};

// Check for stalls using `currentTime` and `readyState`
const startStallCheck = () => {
  console.log("[VideoPlayer.vue] Starting stall check...");
  lastTime = videoPlayerRef.value?.currentTime || 0;

  stallCheckInterval = setInterval(() => {
    if (videoPlayerRef.value) {
      const currentTime = videoPlayerRef.value.currentTime;
      const readyState = videoPlayerRef.value.readyState;

      console.log(`[VideoPlayer.vue] Stall check — currentTime: ${currentTime}, lastTime: ${lastTime}, readyState: ${readyState}`);

      if (currentTime === lastTime && readyState < 3) {
        console.warn("[VideoPlayer.vue] Detected stall — retrying...");
        handleStall();
      } else {
        lastTime = currentTime;
      }
    }
  }, CHECK_INTERVAL);
};

// Stop checking for stalls
const stopStallCheck = () => {
  console.log("[VideoPlayer.vue] Stopping stall check...");
  if (stallCheckInterval) clearInterval(stallCheckInterval);
};

watch(
  () => videoPlayerRef.value?.paused,
  (paused) => {
    console.log(`[VideoPlayer.vue] Paused state changed: ${paused}`);
    if (paused) setupInactivityWatch();
  }
);

onMounted(async () => {
  console.log("[VideoPlayer.vue] Component mounted, calling getNext()");
  await retryAction(attemptGetNext);

  if (videoPlayerRef.value) {
    console.log("[VideoPlayer.vue] Adding event listeners...");
    videoPlayerRef.value.addEventListener("error", handleError);
    videoPlayerRef.value.addEventListener("play", () => {
      console.log("[VideoPlayer.vue] Video playing...");
      setupInactivityWatch();
      startStallCheck();
    });
    videoPlayerRef.value.addEventListener("pause", () => {
      console.log("[VideoPlayer.vue] Video paused...");
      setupInactivityWatch();
      stopStallCheck();
    });
    videoPlayerRef.value.addEventListener("stalled", handleStall);
  }
});

onUnmounted(() => {
  console.log("[VideoPlayer.vue] Component unmounted, stopping retries...");
  stopped = true;
  if (abortController) {
    console.log("[VideoPlayer.vue] Aborting current request...");
    abortController.abort();
  }
  if (inactivityTimeout) {
    console.log("[VideoPlayer.vue] Clearing inactivity timeout...");
    clearTimeout(inactivityTimeout);
  }
  stopStallCheck();
});
</script>

<template>
  <video
    ref="videoPlayerRef"
    class="flex aspect-w-16 aspect-h-9 min-h-[calc(100vw*9/16)]"
    @ended="retryAction(attemptGetNext)"
    autoplay
  >
    <source :src="videoURL" type="video/mp4" />
  </video>
</template>
