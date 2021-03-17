<template style="background-color:#5848b7">
  <div>
    <el-row>
      <el-col :span="4">
        <el-input
          v-model="search"
          @input="filter()"
          placeholder="Ricerca per Cognome"
        >
        </el-input>
      </el-col>

      <el-col :span="20">
        <el-select
          v-model="value"
          @change="filter()"
          clearable
          placeholder="Anno d'iscrizione"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option
        ></el-select>
      </el-col>
    </el-row>
    <el-table
      :data="students"
      style="width:100%;"
      border
      max-height="840px"
      :header-cell-style="tableHeaderColor"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-row class="fill-height">
            <el-col class="md-2">
              <h5 style="font-weight:bold;color:#03396c">Matricola:</h5>
              <p>{{ props.row.matricola }}</p>
              <h5 style="font-weight:bold;color:#03396c">Anno:</h5>
              <p>{{ props.row.anno_iscrizione }}</p>
              <h5 style="font-weight:bold;color:#03396c">Facoltà:</h5>
              <p>{{ props.row.facolta }}</p>
            </el-col>
          </el-row>
        </template>
      </el-table-column>
      <el-table-column label="Nome" prop="nome"> </el-table-column>
      <el-table-column label="Cognome" prop="cognome" sortable>
      </el-table-column>
      <el-table-column label="Email" prop="email"> </el-table-column>
      <el-table-column label="Info">
        <template slot-scope="props">
          <el-button
            type="success"
            size="mini"
            @click="
              dialogVisible = true;
              getExams(props.row.id);
              dialog_title = props.row.nome + ' ' + props.row.cognome;
            "
            >ESAMI</el-button
          >
          <el-button
            type="danger"
            size="mini"
            @click="
              statVisible = true;
              dialog_title = props.row.nome + ' ' + props.row.cognome;
              getStat(props.row.id);
            "
            >ALTRO</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      layout="prev, pager, next"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :total="this.len"
    >
    </el-pagination>
    <el-dialog :visible.sync="dialogVisible" width="70%" center="True">
      <span slot="title">Esami superati da {{ this.dialog_title }}</span>
      <span>
        <el-table
          :data="exams"
          max-height="500px"
          :header-cell-style="tableHeaderColor"
        >
          <el-col>
            <el-table-column label="Voto" prop="voto"></el-table-column>
            <el-table-column
              label="Esame"
              prop="insegnamento"
            ></el-table-column>
            <el-table-column label="Tipo" prop="tipo_esame"></el-table-column>
            <el-table-column label="Data" prop="data"></el-table-column>
          </el-col>
        </el-table>
      </span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false"
          >Chiudi</el-button
        >
      </span>
    </el-dialog>
    <el-dialog
      :visible.sync="statVisible"
      width="70%"
      center="True"
      max-height="500px"
    >
      <span slot="title">Ulteriori info su {{ this.dialog_title }}</span>
      <span>
        <el-table :data="stats" :header-cell-style="tableHeaderColor">
          <el-table-column label="Insegnamento" prop="esame"></el-table-column>
          <el-table-column label="Tipo" prop="tipo"></el-table-column>
          <el-table-column
            label="Tentativi falliti"
            prop="tentativi"
          ></el-table-column>
          <el-table-column
            label="Data ultimo voto rifiutato"
            prop="data_rifiuto"
          ></el-table-column>
          <el-table-column label="Voto" prop="voto"></el-table-column>
        </el-table>
      </span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="statVisible = false"
          >Chiudi</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      students: null,
      exams: null,
      stats: null,
      len: "",
      ricevimenti: "",
      dialogVisible: false,
      statVisible: false,
      dialog_title: "",
      search: "",
      options: "",
      value: "",
      currentPage: 1
    };
  },
  mounted() {
    axios
      .get(
        "./server/api/totale_studenti?cognome=" +
          this.search +
          "&iscrizione=" +
          this.value
      )
      .then(response => (this.len = response.data));
    axios
      .get("./server/api/studente?page=0")
      .then(response => (this.students = response.data.json_list));
    axios
      .get("./server/api/anno_iscrizione")
      .then(response => (this.options = response.data));
  },
  methods: {
    handleCurrentChange(val) {
      this.currentPage = val;
      axios
        .get(
          "./server/api/studente?page=" +
            (this.currentPage - 1).toString() +
            "&cognome=" +
            this.search +
            "&iscrizione=" +
            this.value
        )
        .then(response => (this.students = response.data.json_list));
    },
    getExams(id) {
      axios
        .get("./server/api/esami_superati_studente?id=" + id)
        .then(response => (this.exams = response.data.json_list));
    },
    filter() {
      this.currentPage = 1;
      axios
        .get(
          "./server/api/studente?cognome=" +
            this.search +
            "&iscrizione=" +
            this.value +
            "&matricola=" +
            this.matricola +
            "&page=" +
            (this.currentPage - 1).toString()
        )
        .then(response => (this.students = response.data.json_list));
      axios
        .get(
          "./server/api/totale_studenti?cognome=" +
            this.search +
            "&iscrizione=" +
            this.value
        )
        .then(response => (this.len = response.data));
    },
    getStat(id) {
      axios
        .get("./server/api/statistiche_studente?id=" + id)
        .then(response => (this.stats = response.data.json_list));
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
