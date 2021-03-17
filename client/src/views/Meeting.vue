<template>
  <div>
    <template>
      <el-select
        v-model="value"
        filterable
        remote
        clearable
        @change="getMeeting"
        focus
        reserve-keyword
        placeholder="Email studente"
        :remote-method="remoteMethod"
        :loading="loading"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
      <el-select
        v-model="tag"
        @change="getMeeting"
        collapse-tags
        multiple
        placeholder="Elenco tag"
      >
        <el-option
          v-for="item in keywords"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </template>
    <el-table
      :data="ricevimenti"
      style="width:100%;"
      border
      max-height="840px"
      :header-cell-style="tableHeaderColor"
    >
      <el-table-column label="Nome" prop="nome"> </el-table-column>
      <el-table-column label="Cognome" prop="cognome"> </el-table-column>
      <el-table-column label="Data" prop="data"> </el-table-column>
      <el-table-column label="Domande" prop="domande">
        <template scope="scope">
          <el-button
            type="primary"
            size="mini"
            @click="
              domande = scope.row.domande;
              domandeVisible = true;
            "
            >DOMANDE</el-button
          >
        </template>
      </el-table-column>
      <el-table-column label="Suggerimenti" prop="suggerimenti">
        <template scope="scope">
          <el-button
            type="warning"
            size="mini"
            @click="
              suggerimenti = scope.row.suggerimenti;
              suggerimentiVisible = true;
            "
            >SUGGERIMENTI</el-button
          >
        </template>
      </el-table-column>
      <el-table-column label="Tag" prop="tag">
        <template scope="scope">
          <el-tag v-for="tag in scope.row.tag" :key="tag" :type="primary">
            {{ tag.nome }}
          </el-tag>
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
    <el-dialog :visible.sync="domandeVisible" center="True">
      <span v-html="this.domande"></span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="domandeVisible = false">Chiudi</el-button>
      </span>
    </el-dialog>
    <el-dialog :visible.sync="suggerimentiVisible" center="True">
      <span v-html="this.suggerimenti"></span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="suggerimentiVisible = false">Chiudi</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      domandeVisible: false,
      suggerimentiVisible: false,
      ricevimenti: "",
      domande: "",
      value: "",
      options: [],
      loading: false,
      list: [],
      len: "",
      currentPage: 1,
      keywords: [],
      tag: []
    };
  },
  mounted() {
    axios
      .get(
        "./server/api/totale_ricevimenti?email=" +
          this.value +
          "&tag=" +
          this.tag
      )
      .then(response => (this.len = response.data));
    axios
      .get("./server/api/lista_ricevimenti?page=0")
      .then(response => (this.ricevimenti = response.data));
    axios
      .get("./server/api/lista_studenti")
      .then(response => (this.list = response.data));
    axios
      .get("./server/api/lista_tag")
      .then(response => (this.keywords = response.data));
  },
  methods: {
    remoteMethod(query) {
      if (query !== "") {
        this.loading = true;
        setTimeout(() => {
          this.loading = false;
          this.options = this.list.filter(item => {
            return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1;
          });
        }, 200);
      } else {
        this.options = [];
      }
    },
    getMeeting() {
      this.currentPage = 1;
      axios
        .get(
          "./server/api/lista_ricevimenti?email=" +
            this.value +
            "&tag=" +
            this.tag +
            "&page=" +
            (this.currentPage - 1).toString()
        )
        .then(response => (this.ricevimenti = response.data));
      axios
        .get(
          "./server/api/totale_ricevimenti?email=" +
            this.value +
            "&tag=" +
            this.tag
        )
        .then(response => (this.len = response.data));
    },
    tableHeaderColor({ rowIndex }) {
      if (rowIndex === 0) {
        return "background-color: #409EFF;color: #fff;font-weight: 500;";
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      axios
        .get(
          "./server/api/lista_ricevimenti?page=" +
            (this.currentPage - 1).toString() +
            "&email=" +
            this.value +
            "&tag=" +
            this.tag
        )
        .then(response => (this.ricevimenti = response.data));
    }
  }
};
</script>

<style></style>
