<template>
  <div style="background-color:#5848b7;">
    <el-select
      v-model="insegnamento"
      clearable
      @change="
        getType();
        clearExam();
      "
      placeholder="Seleziona il corso"
    >
      <el-option
        v-for="item in courses"
        :key="item"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>
    <el-select
      v-show="this.insegnamento == '' ? (disabled = false) : (disabled = true)"
      v-model="tipo"
      @change="
        getYear();
        clearExam();
      "
      clearable
      placeholder="Seleziona il tipo di esame"
    >
      <el-option v-for="item in type" :key="item" :label="item" :value="item">
      </el-option>
    </el-select>
    <el-select
      v-show="
        this.insegnamento == '' || this.tipo == ''
          ? (disabled = false)
          : (disabled = true)
      "
      v-model="year"
      @change="
        clearExam();
        getAllData();
      "
      clearable
      placeholder="Seleziona l'anno"
    >
      <el-option v-for="item in years" :key="item" :label="item" :value="item">
      </el-option>
    </el-select>
    <el-select
      v-show="
        this.insegnamento == '' || this.tipo == '' || this.year == ''
          ? (disabled = false)
          : (disabled = true)
      "
      v-model="data"
      @change="
        clearExam();
        getAllExams();
      "
      placeholder="Seleziona l'esame"
    >
      <el-option v-for="item in dates" :key="item" :label="item" :value="item">
      </el-option>
    </el-select>
    <el-table :data="exams" border :header-cell-style="tableHeaderColor">
      <el-table-column
        label="Cognome"
        prop="cognome"
        sortable
      ></el-table-column>
      <el-table-column label="Nome" prop="nome"></el-table-column>
      <el-table-column
        label="Matricola"
        prop="matricola"
        resizable
      ></el-table-column>
      <el-table-column label="Esito" prop="esito" resizable></el-table-column>
      <el-table-column
        label="Voto"
        prop="voto"
        sortable
        resizable
      ></el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      insegnamento: "",
      tipo: "",
      data: "",
      year: "",
      courses: null,
      type: null,
      exams: "",
      dates: null,
      years: null
    };
  },
  mounted() {
    axios
      .get("./server/api/insegnamenti")
      .then(response => (this.courses = response.data));
  },
  methods: {
    clearExam() {
      this.exams = "";
    },
    getType() {
      this.tipo = "";
      if (this.insegnamento != "")
        axios
          .get("./server/api/modalita_esame?insegnamento=" + this.insegnamento)
          .then(response => (this.type = response.data.json_list));
    },
    getYear() {
      this.year = "";
      if (this.tipo != "")
        axios
          .get(
            "./server/api/appelli?insegnamento=" +
              this.insegnamento +
              "&tipo=" +
              this.tipo
          )
          .then(response => (this.years = response.data.json_list));
    },
    getAllData() {
      this.data = "";
      if (this.year != "")
        axios
          .get(
            "./server/api/date_appelli?insegnamento=" +
              this.insegnamento +
              "&tipo=" +
              this.tipo +
              "&anno=" +
              this.year
          )
          .then(response => (this.dates = response.data.json_list));
    },
    formatDate(date) {
      var d = new Date(date),
        month = "" + (d.getMonth() + 1),
        day = "" + d.getDate(),
        year = d.getFullYear();

      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;

      return [year, month, day].join("-");
    },
    getAllExams() {
      this.data = this.formatDate(this.data);
      axios
        .get(
          "./server/api/risultati_esame?insegnamento=" +
            this.insegnamento +
            "&tipo=" +
            this.tipo +
            "&data=" +
            this.data
        )
        .then(response => (this.exams = response.data.json_list));
    },
    tableHeaderColor({ rowIndex }) {
      if (rowIndex === 0) {
        return "background-color: #409EFF;color: #fff;font-weight: 500;";
      }
    }
  }
};
</script>

<style></style>
