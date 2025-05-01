type AuthType = "seat" | "survey" | "award";
interface ClassItem {
  教室: string;
  內容: string;
  時間: string;
  共補: number;
}
interface classWithSeats {
  text?: string;
}
interface RateableEmployee {
  學號: string;
  姓名: string;
  主要部門: string;
}
interface userData {
  學號: string;
  姓名: string;
  性別: "男" | "女";
  rateable_employees: RateableEmployee[];
}
const example = {
  學號: "300003",
  姓名: "邱小傑1",
  性別: "男",
  rateable_employees: [
    {
      學號: "200860",
      姓名: "林子軒",
      主要部門: "數輔",
    },
    {
      學號: "201125",
      姓名: "簡延叡",
      主要部門: "導師組",
    },
    {
      學號: "201171",
      姓名: "唐冠霖",
      主要部門: "導師組",
    },
    {
      學號: "201199",
      姓名: "簡翊軒",
      主要部門: "招生部",
    },
    {
      學號: "201206",
      姓名: "李佳穎",
      主要部門: "數輔",
    },
    {
      學號: "201209",
      姓名: "毛翊嘉",
      主要部門: "數輔",
    },
    {
      學號: "201271",
      姓名: "郭力銘",
      主要部門: "數輔",
    },
    {
      學號: "201272",
      姓名: "黃瑀緹",
      主要部門: "櫃台",
    },
    {
      學號: "201324",
      姓名: "鄭安妍",
      主要部門: "櫃台",
    },
    {
      學號: "201292",
      姓名: "潘嘉韻",
      主要部門: "導師組",
    },
    {
      學號: "201305",
      姓名: "陸君維",
      主要部門: "導師組",
    },
    {
      學號: "201331",
      姓名: "蔡昇祐",
      主要部門: "導師組",
    },
    {
      學號: "201332",
      姓名: "鄭昀昕",
      主要部門: "招生部",
    },
    {
      學號: "201308",
      姓名: "胡家晉",
      主要部門: "補課教室",
    },
    {
      學號: "201365",
      姓名: "劉少騏",
      主要部門: "導師組",
    },
    {
      學號: "201375",
      姓名: "陳宣瑋",
      主要部門: "補課教室",
    },
    {
      學號: "201386",
      姓名: "游佳璇",
      主要部門: "導師組",
    },
    {
      學號: "201385",
      姓名: "江念庭",
      主要部門: "導師組",
    },
  ],
};
import { reactive } from "vue";
export const store = reactive<{
  authType: AuthType;
  authStudentId: string;
  authBackspace: () => void;
  checkSeatsAvailbility: () => boolean;
  classesToday: ClassItem[];
  classWithSeats: classWithSeats;
  dialogMessage: string;
  dialogClass: string;
  dialogVisibility: boolean;
  setupDialog: (
    severity: "error" | "loading" | "success",
    message: string
  ) => void;
  showDialog: () => void;
  closeDialog: () => void;
  surveyIs4Math: boolean;
  userData: userData;
  clearUserData: () => void
}>({
  authType: "survey", // must be one of "id", "qrcode", "manual"
  authStudentId: "",
  authBackspace() {
    store.authStudentId = store.authStudentId.slice(0, -1);
  },
  checkSeatsAvailbility() {
    if (Object.keys(store.classWithSeats).length === 0) {
      return false;
    } else {
      return true;
    }
  },
  classesToday: [],
  classWithSeats: {},
  dialogMessage: "",
  dialogClass: "",
  dialogVisibility: false,
  setupDialog(severity, message) {
    switch (severity) {
      case "error":
        store.dialogClass = "pi pi-times-circle";
        break;
      case "loading":
        store.dialogClass = "pi pi-spin pi-spinner";
        break;
      case "success":
        store.dialogClass = "pi pi-check-circle";
        break;
      default:
        store.dialogClass = "";
    }

    store.dialogMessage = message;
  },
  showDialog() {
    store.dialogVisibility = true;
  },
  closeDialog() {
    store.dialogVisibility = false;
    store.dialogMessage = "";
    store.dialogClass = "";
  },
  surveyIs4Math: false,
  userData: {
    學號: "000000",
    姓名: "XXX",
    性別: "男",
    rateable_employees: [],
  },
  clearUserData() {
    store.authType = "survey", // must be one of "id", "qrcode", "manual"
  store.authStudentId= "",
    store.userData = {
        學號: "000000",
        姓名: "XXX",
        性別: "男",
        rateable_employees: [],
      }
  }
});
