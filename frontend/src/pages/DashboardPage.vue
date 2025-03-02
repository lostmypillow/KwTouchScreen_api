<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useToast } from "primevue/usetoast";
import axios from "axios";
const toast = useToast();

// VIDEO logic
const videoList = ref(["No files present on disk"]);
const selectedVideo = ref("");
const isUploading = ref(false);
const isDeleting = ref(false);

// Retry logic helper function
const retryRequest = async (fn, retries = 3, delay = 2000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      if (i < retries - 1) await new Promise((res) => setTimeout(res, delay));
    }
  }
  throw new Error("All retry attempts failed");
};

const getVideoList = async () => {
  try {
    videoList.value = await retryRequest(async () => {
      return (await axios.get(`http://${import.meta.env.VITE_VIDEO_URL}/all/`)).data;
    });
    toast.add({
      severity: "success",
      summary: "Fetch Successful",
      detail: "Video list updated",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Fetch Failed",
      detail: "Video list failed to update",
      life: 3000,
    });
  }
};

const onFileSelect = async (event) => {
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
    toast.add({
      severity: "success",
      summary: "Upload Complete",
      detail: "File upload done",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upload Failed",
      detail: "File upload failed after retries",
      life: 3000,
    });
  } finally {
    isUploading.value = false;
  }
};

const deleteVid = async () => {
  isDeleting.value = true;
  const f = selectedVideo.value.toString();

  try {
    await retryRequest(() => axios.delete(`http://${import.meta.env.VITE_VIDEO_URL}/video/${f}`));
    toast.add({
      severity: "success",
      summary: "Deletion Complete",
      detail: "File deleted",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Deletion Failed",
      detail: "File deletion failed after retries",
      life: 3000,
    });
  } finally {
    isDeleting.value = false;
    selectedVideo.value = "";
  }
};
// VIDEO logic end

const connectedToServer = ref(false);
const ws = ref(null);

const initWs = () => {
  const connectWebSocket = () => {
    ws.value = new WebSocket(`ws://${import.meta.env.VITE_SERVER_URL}/ws/control`);
    console.log(`Attempting WebSocket connection...`);

    ws.value.onopen = () => {
      console.log("WebSocket connected");
      connectedToServer.value = true;
    };

    ws.value.onmessage = (event) => {
      console.log("Message received", event.data);
    };

    ws.value.onerror = (error) => {
      console.error("WebSocket error: ", error);
      connectedToServer.value = false;
      ws.value.close();
    };

    ws.value.onclose = () => {
      console.log("WebSocket disconnected, retrying in 3s...");
      connectedToServer.value = false;
      setTimeout(connectWebSocket, 3000);
    };
  };

  connectWebSocket();
};

onMounted(async () => {
  initWs();
  await getVideoList();
});

onUnmounted(() => {
  if (ws.value) {
    ws.value.close();
    console.log("WebSocket closed on unmount");
  }
});
</script>


<template>
  <main class="flex flex-col p-4">
    <div>
      <h1 class="text-3xl font-extrabold mb-4">Dashboard</h1>
    </div>
    <div
      class="flex md:flex-row md:flex-wrap flex-col md:items-start md:justify-start items-center justify-center"
    >
      <div class="md:w-1/4 w-full p-4">
        <Card>
          <template #title>Connection Status</template>
          <template #content>
            <p class="m-0">
              <span
                :class="[connectedToServer ? 'text-green-500' : 'text-red-500']"
                >{{ connectedToServer ? "Connected" : "NOT connected" }}</span
              >
              to FastAPI WebSocket
            </p>
          </template>
          <template #footer>
            <Button
              :disabled="isConnected"
              label="Refresh Connection"
              class="w-full"
            />
          </template>
        </Card>
      </div>
    

      <div class="md:w-1/4 w-full p-4">
        <Card>
          <template #title>
            <div class="flex w-full items-center justify-between gap-4">
              Videos
              <Button
                :disabled="!selectedVideo || isDeleting"
                label="Delete"
                severity="danger"
                @click="deleteVid"
              />
            </div>
          </template>
          <template #content>
            <Listbox
              v-model="selectedVideo"
              :options="videoList"
              class="w-full"
            />
          </template>
          <template #footer>
            <div class="flex flex-col gap-4 mt-1">
              <Toast />
              <FileUpload
                icon="pi pi-cloud-upload"
                :disabled="isUploading"
                mode="basic"
                customUpload
                @select="onFileSelect"
                accept="video/*"
                :chooseLabel="isUploading ? 'Uploading...' : 'Upload more'"
                >
                
                <template #empty><i class="pi pi-cloud-upload"></i></template>
                
               
              </FileUpload>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </main>
</template>

<style scoped>
.p-fileupload span {
  display: none;
}
</style>
