<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useToast } from "primevue/usetoast";
import axios from "axios";
const toast = useToast();

const onFileSelect = async (event) => {
  const file = event.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    await axios.post(`http://${window.location.host}/video/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    toast.add({
      severity: "success",
      summary: "Upload Complete",
      detail: "File upload done",
      life: 3000,
    });
  } catch (error) {
    console.error(error);
    toast.add({
      severity: "error",
      summary: "Upload Failed",
      detail: "File upload failed",
      life: 3000,
    });
  }
};
const connectedToServer = ref(false);
const connectedToClient = ref(false);
const videoList = ref(["meow", "meow2"]);
const selectedVideo = ref("");
const isUploading = ref(false);

const isConnected = ref(true);
const classesToday = ref([]);
const classWithSeats = ref({
  主檔號: 0,
  班級名稱: "",
  班別: "",
  男座位: [],
  女座位: [],
});
const ws = ref(null);
const initWs = () => {
  ws.value = new WebSocket(`ws://${window.location.host}/ws/control`);
  console.log(`ws://${window.location.host}/ws/control`);

  // On WebSocket open, set connection state to true
  ws.value.onopen = () => {
    console.log("WebSocket connected");
    connectedToServer.value = true;
  };

  // On WebSocket message, update server connection state
  ws.value.onmessage = (event) => {
    console.log("Message received");
    const message = JSON.parse(event.data);
    if (message.action == "update queue") {
      videoList.value = message.message;
    } else if (message.action == "update client status") {
      connectedToClient.value = message.message == "connected" ? true : false;
    } else if (message.action == "update class") {
      classesToday.value = message.message.classes_today
      classWithSeats.value = message.message.class_with_seats
    } else {
      console.log(message);
    }
  };

  // On WebSocket error, set connection state to false
  ws.value.onerror = (error) => {
    console.error("WebSocket error: ", error);
    connectedToServer.value = false;
    ws.close();
  };

  // On WebSocket close, set connection state to false and prepare for reconnection
  ws.value.onclose = () => {
    console.log("WebSocket disconnected");
    connectedToServer.value = false;
  };
};
onMounted(() => initWs());
onUnmounted(() => {
  if (ws.value) {
    ws.value.close();
    console.log("WebSocket closed on unmount");
  }
});
const isDeleting = ref(false);
const deleteVid = async () => {
  isDeleting.value = true;
  const f = selectedVideo.value.toString().replace(".mp4", "");
  try {
    await axios.delete(`http://${window.location.host}/video/${f}`);
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
      detail: "File deletion failed",
      life: 3000,
    });
  } finally {
    isDeleting.value = false;
    selectedVideo.value = ''
  }
};
</script>

<template>
  <main class="p-4">
    <h1 class="text-3xl font-bold mb-4">觸控螢幕 API / KwTouchScreen API</h1>
    <div
      class="flex md:flex-row md:flex-wrap flex-col items-start justify-start"
    >
      <div class="w-1/4 p-4">
        <Card v-if="classesToday">
          <template #title>Classes Today</template>
          <template #content>
            <DataTable :value="classesToday">
              <Column field="教室" header="教室"></Column>
              <Column field="內容" header="內容"></Column>
              <Column field="時間" header="時間"></Column>
              <Column field="共補" header="共補"></Column>
            </DataTable>
          </template>
        </Card>
      </div>

      <div class="w-1/4 p-4">
        <Card>
          <template #title>Class With Seats</template>
          <template #content>
            <h2 class="text-xl">
              {{ classWithSeats.班別 + " (" + classWithSeats.班級名稱 + ")" }}
            </h2>
            <p>主檔號: {{ classWithSeats.主檔號 }}</p>
            <p>
              男座位剩餘 {{ classWithSeats.男座位.length }} 、女座位剩餘
              {{ classWithSeats.女座位.length }}
            </p>
          </template>
        </Card>
      </div>

      <div class="w-1/4 p-4">
        <Card>
          <template #title>Connection Status</template>
          <template #content>
            <p class="m-0">
              <span
                :class="[connectedToServer ? 'text-green-500' : 'text-red-500']"
                >{{ connectedToServer ? "Connected" : "NOT connected" }}</span
              >
              to FastAPI WebSocket
              <br />
              <span
                :class="[connectedToClient ? 'text-green-500' : 'text-red-500']"
                >{{ connectedToClient ? "Connected" : "NOT connected" }}</span
              >
              to Android touch kiosk
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

      <div class="w-1/4 p-4">
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
                :disabled="isUploading"
                mode="basic"
                customUpload
                @select="onFileSelect"
                accept="video/*"
                chooseLabel="Upload more"
              />
              
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
