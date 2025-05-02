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
interface ScholarshipDates {
  ssd_id: string;
  year: number;
  semester: number;
  times: number;
  scholarship_items: ScholarshipItems[];
}
interface ScholarshipItems {
  ssi_id: string;
  name: string;
  money: number;
  start_time: string;
  end_time: string;
  classes: ScholarshipClasses[];
}
interface ScholarshipClasses {
  class_id: string;
  class_name: string;
}
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
  clearUserData: () => void;
  scholarshipDates: ScholarshipDates[];
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
    store.authType = "survey"
    store.authStudentId = ""
    store.surveyIs4Math = false
    store.userData = {
      學號: "000000",
      姓名: "XXX",
      性別: "男",
      rateable_employees: [],
    };
  },
  scholarshipDates: [
    {
      ssd_id: "",
      year: 0,
      semester: 0,
      times: 0 ,
      scholarship_items: [
        {
          ssi_id: "",
          name: "",
          money: 0,
          start_time: "",
          end_time: "",
          classes: [
            {
              class_id: "",
              class_name: "",
            },
          ],
        },
      ],
    },
  ],
});

