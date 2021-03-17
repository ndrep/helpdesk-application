<template>
  <el-tabs type="card" style="background-color:el-tabs el-tabs--top">
    <el-tab-pane>
      <span slot="label" style="color:white"
        ><i class="el-icon-s-custom"></i> Studenti</span
      >
      <students></students>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label" style="color:white"
        ><i class="el-icon-notebook-1"></i> Esami</span
      >
      <exams></exams>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label" style="color:white"
        ><i class="el-icon-s-comment"></i> Ricevimenti</span
      >
      <meeting></meeting>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label" style="color:white"
        ><i class="el-icon-tickets"></i>Frequenza Lezioni</span
      >
      <frequence></frequence>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label">
        <el-link style="color:white;" href="./server/">Admin</el-link>
      </span>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import Students from "../views/Students";
import Exams from "../views/Exams";
import Meeting from "../views/Meeting";
import Frequence from "../views/Frequence";

export default {
  data() {
    return {};
  },
  components: {
    Students,
    Exams,
    Meeting,
    Frequence
  }
};
</script>

<style>
.el-tabs__nav-scroll {
  background-color: #5848b7;
}
.el-tabs--top {
  background-color: #5848b7;
}
</style>
