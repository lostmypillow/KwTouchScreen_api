<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { store } from "../store";
import { useLogger } from "../composables/useLogger";
const logger = useLogger();
const videoList = ref(["No files present on disk"]);
const selectedVideo = ref("");
const isUploading = ref(false);
const isDeleting = ref(false);
const connectedToServer = ref(false);

const showAndLogError = (message, error) => {
  logger.error(`${message} ${JSON.stringify(error)}`);
  store.setupDialog("error", `${message} ${JSON.stringify(error)}`);
};

const showAndLogSuccess = (message) => {
  logger.info(message);
  store.setupDialog("success", message);
};
// Retry logic
const retryRequest = async (fn, retries = 3, delay = 2000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      logger.info(
        `Attempt ${i + 1} failed, ${
          typeof error === "string" ? error : JSON.stringify(error)
        }`
      );
      if (i < retries - 1) await new Promise((res) => setTimeout(res, delay));
    }
  }
  throw new Error("All retry attempts failed");
};

const getVideoList = async () => {
  store.setupDialog("loading", "Fetching video list");
  store.showDialog();
  try {
    videoList.value = await retryRequest(async () => {
      return (await axios.get(`http://${import.meta.env.VITE_VIDEO_URL}/all/`))
        .data;
    });
    showAndLogSuccess("Video list updated");
  } catch (error) {
    showAndLogError("Video list update failed", error);
  } finally {
    setTimeout(() => store.closeDialog(), 3000);
  }
};

const onFileSelect = async (event) => {
  store.setupDialog("loading", "Uploading files");
  store.showDialog();
  const file = event.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);
  isUploading.value = true;

  try {
    await retryRequest(() =>
      axios.post(`http://${import.meta.env.VITE_VIDEO_URL}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
    );
    showAndLogSuccess(`${file.name} File upload done`);
    await getVideoList();
  } catch (error) {
    showAndLogError("Upload video failed", error);
  } finally {
    setTimeout(() => store.closeDialog(), 3000);
  }
};

const deleteVid = async () => {
  store.setupDialog("loading", "Deleting files");
  store.showDialog();
  isDeleting.value = true;
  const f = selectedVideo.value.toString();

  try {
    await retryRequest(() =>
      axios.delete(`http://${import.meta.env.VITE_VIDEO_URL}/video/${f}`)
    );

    showAndLogSuccess(`${f} Video deleted`);
    await getVideoList();
  } catch (error) {
    showAndLogError("File deletion failed", error);
  } finally {
    selectedVideo.value = "";
    setTimeout(() => store.closeDialog(), 3000);
  }
};

onMounted(async () => await getVideoList());
</script>

<template>
  <main class="flex flex-col w-full p-4">
    <div class="flex items-center justify-between gap-4 p-4">
      <h2 class="text-2xl">Videos</h2>
      <div class="flex flex-row gap-2">
        <FileUpload
        icon="pi pi-cloud-upload"
        :disabled="isUploading"
        mode="basic"
        customUpload
        @select="onFileSelect"
        accept="video/*"
        :chooseLabel="isUploading ? 'Uploading...' : 'Upload more'"
      >
      </FileUpload>
      
  
      <Button
        :disabled="!selectedVideo"
        label="Delete"
        severity="danger"
        @click="deleteVid"
      />
      </div>
      
    </div>

    <Listbox v-model="selectedVideo" :options="videoList" class="w-full max-h-full" />


  </main>
</template>

<style scoped>
.p-fileupload span {
  display: none;
}
:deep(.p-listbox-list-container) {
  max-height: 100% !important
}
</style>
