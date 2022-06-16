<template>
  <AnnotateViewLoadedPage v-if="isLoaded"/>
  <div v-else style="position: relative;">
    <el-tabs>
      <el-tab-pane label="我创建的任务">
        <team-task-table/>
      </el-tab-pane>

      <el-tab-pane label="我接受的任务">
        <team-subtask-table/>
      </el-tab-pane>
    </el-tabs>
    <div class="button-wrap">
      <el-button
          size="medium"
          type="primary"
          @click="dialogVisible=true"
          plain
      >
        创建多人任务
      </el-button>
    </div>
    <team-task-create-dialog :dialog-visible.sync="dialogVisible"/>
  </div>
</template>

<script>
import TeamTaskCreateDialog from "@/components/TeamTaskCreateDialog";
import TeamTaskTable from "@/components/TeamTaskTable";
import TeamSubtaskTable from "@/components/TeamSubtaskTable";
import AnnotateViewLoadedPage from "@/components/AnnotateViewLoadedPage";
export default {
  name: "TeamTaskView",
  components:{
    TeamTaskCreateDialog,
    TeamTaskTable,
    TeamSubtaskTable,
    AnnotateViewLoadedPage
  },
  data(){
    return {
      dialogVisible: false
    }
  },
  computed:{
    isLoaded() {
      return !!this.$store.state.annotate.datasetID;
    }
  },
  created() {
    this.$store.commit('annotate/setDatasetID', '')
    this.$store.dispatch('teamTask/getTeamTasks')
    this.$store.dispatch('teamTask/getSubTasks')
  }

}
</script>

<style scoped>
.button-wrap{
  position: absolute;
  right: 10px;
  top: -2px;
}
</style>