import { reactive } from "vue";

export const surveyStore = reactive({
  selectedDepartment: {},
  selectedEmployee: {},
  employeeID: null,
  rating: null,
  clear() {
    this.selectedDepartment = {};
    this.selectedEmployee = {};
    this.employeeID = null;
    this.rating = null;
  },

  allEmployees: [],
  setEmployees(employees) {
    this.allEmployees = employees;
  },
  departmentList() {
    const departments = new Map();
    this.allEmployees.forEach((item) => {
      if (item.department_number != 9) {
        // Use the department_number as the unique key
        departments.set(item.department_number, {
          name: item.department_name,
          number: item.department_number,
        });
      }
    });
    return [...departments.values()]; 
  },
  setDepartment(department) {
    this.selectedDepartment = department;
  },
  setEmployee(employee) {
    this.selectedEmployee = employee;
  },
  filteredEmployees(item) {
    return this.allEmployees.filter(
      (item) => item.department_number == this.selectedDepartment.number
    );
  },
  hasNoDepartment() {
    return this.selectedDepartment.name == undefined;
  },
  hasNoEmployee() {
    return this.selectedEmployee.name == undefined;
  },
  resetDepartment() {
    this.selectedDepartment = {};
    this.selectedEmployee = {};
    this.rating = null
  },
  resetEmployee() {
    this.selectedEmployee = {};
    this.rating = null
  },
  showRating() {
    return (
      this.selectedDepartment.name !== undefined &&
      this.selectedEmployee.name !== undefined
    );
  },
  allFinished() {
    return (
      this.selectedDepartment.name != undefined &&
      this.selectedEmployee.name != undefined &&
      this.rating != null
    );
  },
});
