<template>
  <div>
    <el-select
      v-model="corso"
      clearable
      @change="
        getAnno();
        clearExam();
      "
      placeholder="Seleziona il corso"
    >
      <el-option
        v-for="item in insegnamenti"
        :key="item"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>
    <el-select
      v-show="this.corso == '' ? (disabled = false) : (disabled = true)"
      v-model="anno"
      @change="
        getTipo();
        clearExam();
      "
      clearable
      placeholder="Seleziona l'anno accademico"
    >
      <el-option
        v-for="item in anno_accademico"
        :key="item"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>

    <el-select
      v-show="
        this.corso == '' || this.anno == ''
          ? (disabled = false)
          : (disabled = true)
      "
      v-model="tipo"
      @change="
        clearExam();
        getPresenze();
      "
      clearable
      placeholder="Tipo lezione"
    >
      <el-option v-for="item in tipi" :key="item" :label="item" :value="item">
      </el-option>
    </el-select>

    <el-table :data="studenti" border :header-cell-style="tableHeaderColor">
      <el-table-column label="Nome" prop="nome"></el-table-column>
      <el-table-column label="Cognome" prop="cognome"></el-table-column>
      <el-table-column label="Totale Lezioni" prop="totale"></el-table-column>
      <el-table-column
        label="Totale Presenze"
        prop="presenze"
      ></el-table-column>
      <el-table-column label="Info">
        <template slot-scope="props">
          <el-button
            type="info"
            size="mini"
            @click="
              dialogVisible = true;
              dialog_title = props.row.nome + ' ' + props.row.cognome;
              getDate(props.row.studente_id);
            "
            >DETTAGLI</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogVisible" width="70%" center="True">
      <span slot="title">Presenze a lezione di {{ this.dialog_title }}</span>
      <span>
        <el-table
          :data="date"
          border
          :header-cell-style="tableHeaderColor"
          :row-class-name="tableRowClassName"
        >
          <el-table-column label="Data" prop="data"></el-table-column>
          <el-table-column label="Presenza" prop="presenza"></el-table-column>
        </el-table>
      </span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false"
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
      insegnamenti: "",
      corso: "",
      anno_accademico: "",
      anno: "",
      tipo: "",
      tipi: "",
      studenti: "",
      dialogVisible: false,
      dialog_title: "",
      date: ""
    };
  },
  mounted() {
    axios
      .get("./server/api/insegnamenti")
      .then(response => (this.insegnamenti = response.data));
  },
  methods: {
    tableHeaderColor({ rowIndex }) {
      if (rowIndex === 0) {
        return "background-color: #409EFF;color: #fff;font-weight: 500;";
      }
    },
    tableRowClassName({ row }) {
      if (row.presenza === "P") {
        return "success-row";
      } else {
        return "warning-row";
      }
    },
    clearExam() {
      this.studenti = "";
    },
    getAnno() {
      this.anno = "";
      if (this.corso != "")
        axios
          .get("./server/api/lista_anni_accademici?insegnamento=" + this.corso)
          .then(response => (this.anno_accademico = response.data));
    },
    getTipo() {
      this.tipo = "";
      if (this.anno != "")
        axios
          .get(
            "./server/api/tipo_lezione?insegnamento=" +
              this.corso +
              "&anno_accademico=" +
              this.anno
          )
          .then(response => (this.tipi = response.data));
    },
    getPresenze() {
      axios
        .get(
          "./server/api/lista_presenze_corso?insegnamento=" +
            this.corso +
            "&anno_accademico=" +
            this.anno +
            "&tipo=" +
            this.tipo
        )
        .then(response => (this.studenti = response.data));
    },
    getDate(studente) {
      axios
        .get(
          "./server/api/date_presenze?studente_id=" +
            studente +
            "&insegnamento=" +
            this.corso +
            "&anno_accademico=" +
            this.anno +
            "&tipo=" +
            this.tipo
        )
        .then(response => (this.date = response.data));
    }
  }
};
</script>

<style>
.el-table .warning-row {
  background: #f56c6c;
  color: white;
}

.el-table .success-row {
  background: #67c23a;
  color: white;
}
</style>
